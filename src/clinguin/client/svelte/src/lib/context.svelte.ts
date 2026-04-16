/**
 * App-wide state and server communication for Clinguin.
 *
 * This file defines the AppContext class, which holds the global state of the app and methods for connecting to the backend, fetching the UI, and handling operations.
 * It uses Svelte's $state for reactivity and is instantiated as a singleton exported as appContext.
 */

import { toWebSocketUrl } from '$lib/utils';

// Fallback used only during direct `npm run dev` without client.py.
// In production, VITE_SERVER_URL is injected at build time by client.py.
const DEFAULT_SERVER_URL = 'http://127.0.0.1:8000';

/**
 * attr/3
 * Example: attr(my_button, label, "Click me").
 */
type ClinguinAttribute = {
  id: string;
  key: string;
  value: string | number | boolean;
};

/**
 * when/4
 * Example: when(my_button, click, call, next_solution).
 *
 * action (e.g. "call", "update", "context")
 * operation: the operation string passed to the backend for "call" actions
 */
type ClinguinWhen = {
  id: string;
  event: string;
  action: string;
  operation?: string;
};

/**
 * elem/3
 * Example: elem(my_button, button, my_window).
 */
type ClinguinNode = {
  id: string;
  type: string;
  parent: string;
  attributes?: ClinguinAttribute[];
  when?: ClinguinWhen[];
  children?: ClinguinNode[];
};

/** Shape of the JSON response from GET /info. */
type InfoResponse = {
  status: string;
  version: number;
  active_sessions: number;
  ui?: ClinguinNode;
  ds?: unknown;
};

class AppContext {
  serverUrl         = $state(import.meta.env.VITE_SERVER_URL || DEFAULT_SERVER_URL);
  sessionId         = $state('');
  version           = $state(1);
  connectionPromise = $state<Promise<void> | null>(null);
  loading           = $state(false);
  error             = $state('');
  ui                = $state<ClinguinNode | null>(null);
  ds                = $state<unknown>(null);

  private ws: WebSocket | null = null;

  connect = () => {
    this.connectionPromise = this._connect();
    return this.connectionPromise;
  };

  /** Opens the WebSocket then fetches the initial UI. Throws on any failure. */
  private _connect = async (): Promise<void> => {
    await this._openWebSocket();
    const data = await this._doFetchInfo();
    this.version = data.version;
    this.ui      = data.ui  ?? null;
    this.ds      = data.ds  ?? null;
  };

  /**
   * Opens a WebSocket connection to /ws.
   * Resolves once the server sends the session_id.
   * Also handles version_update messages from the server — triggered when
   * another client performs an operation in single-backend mode.
   */
  private _openWebSocket = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      const wsUrl  = `${toWebSocketUrl(this.serverUrl)}/ws`;
      this.ws      = new WebSocket(wsUrl);

      this.ws.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        if (data.session_id) {
          this.sessionId = data.session_id;
          resolve();
          return;
        }
        if (data.type === 'version_update') {
          this.version = data.new_version;
          await this.fetchInfo();
        }
      };

      this.ws.onerror = () => reject(new Error('WebSocket connection failed.'));
      this.ws.onclose = () => { this.ws = null; };
    });
  };

  /**
   * Core HTTP fetch for GET /info.
   * Throws on failure — callers decide how to handle the error.
   * Requires sessionId to be set before calling.
   */
  private _doFetchInfo = async (): Promise<InfoResponse> => {
    if (!this.sessionId) throw new Error('Missing session ID.');
    const response = await fetch(`${this.serverUrl}/info`, {
      method: 'GET',
      headers: { 'session-id': this.sessionId }
    });
    if (!response.ok) throw new Error(`GET /info failed with status ${response.status}`);
    return response.json();
  };

  /**
   * Public wrapper around _doFetchInfo.
   * Sets loading/error state — used after version_update and after callOperation.
   */
  fetchInfo = async (): Promise<void> => {
    this.loading = true;
    this.error   = '';
    try {
      const data   = await this._doFetchInfo();
      this.version = data.version;
      this.ui      = data.ui  ?? null;
      this.ds      = data.ds  ?? null;
    } catch (err) {
      this.error = err instanceof Error ? err.message : 'Unknown error while fetching UI.';
    } finally {
      this.loading = false;
    }
  };

  /**
   * Routes a when/4 action to the appropriate handler.
   * Currently only "call" is implemented — it sends the operation to the backend.
   *
   * TODO: implement "update" and "context"
   */
  handleWhen = async (when: ClinguinWhen): Promise<void> => {
    if (!when) return;
    switch (when.action) {
      case 'call':
        if (!when.operation) return;
        await this.callOperation(when.operation);
        return;
      default:
        console.warn('Unsupported action:', when);
    }
  };

  /**
   * Sends a POST /operation request to the backend.
   * Includes the current version for conflict detection.
   * On 409 (version conflict), syncs with the latest UI before rethrowing.
   * On success, fetches the updated UI.
   */
  callOperation = async (operation: string): Promise<void> => {
    this.loading = true;
    this.error   = '';
    try {
      const response = await fetch(`${this.serverUrl}/operation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'session-id':   this.sessionId
        },
        body: JSON.stringify({ operation, client_version: this.version })
      });

      if (response.status === 409) {
        await this.fetchInfo();
        throw new Error('Client version outdated. Synced with latest UI.');
      }
      if (!response.ok) throw new Error(`POST /operation failed with status ${response.status}`);

      const data   = await response.json();
      this.version = data.version ?? this.version;
      await this.fetchInfo();
    } catch (err) {
      this.error = err instanceof Error ? err.message : 'Unknown error while executing operation.';
    } finally {
      this.loading = false;
    }
  };
}

export const appContext = new AppContext();
export type { ClinguinNode, ClinguinWhen, ClinguinAttribute };
