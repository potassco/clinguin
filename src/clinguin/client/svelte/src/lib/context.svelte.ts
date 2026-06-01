/**
 * App-wide state and server communication for Clinguin.
 *
 * This file defines the AppContext class, which holds the global state of the app and methods for connecting to the backend, fetching the UI, and handling operations.
 * It uses Svelte's $state for reactivity and is instantiated as a singleton exported as appContext.
 */

import { toWebSocketUrl } from '$lib/utils';
import type { AppError } from '$lib/types';

// Fallback used only during direct `npm run dev` without client.py.
// In production, VITE_SERVER_URL is injected at build time by client.py.
const DEFAULT_SERVER_URL = 'http://127.0.0.1:8000';
import type { ClinguinNode, ClinguinWhen, InfoResponse, ClinguinAttribute } from '$lib/types';

class AppContext {
  serverUrl = $state(import.meta.env.VITE_SERVER_URL || DEFAULT_SERVER_URL);
  sessionId = $state('');
  version = $state(1);
  connectionPromise = $state<Promise<void> | null>(null);
  loading = $state(false);
  ui = $state<ClinguinNode | null>(null);
  ds = $state<unknown>(null);
  connected = $state(false);

  private ws: WebSocket | null = null;

  error = $state<AppError | null>(null);

  private _errorMessage = (err: unknown): string =>
    err instanceof Error ? err.message : 'Unknown error.';


  connect = () => {
    this.connectionPromise = this._connect();
    return this.connectionPromise;
  };

  /** Opens the WebSocket then fetches the initial UI. Throws on any failure. */
  private _connect = async (): Promise<void> => {
    await this._openWebSocket();
    const data = await this._doFetchInfo();
    this.version = data.version;
    this.ui = data.ui ?? null;
    this.ds = data.ds ?? null;
    this.connected = true;  // set once, never reset
  };

  private _extractErrorMessage = async (response: Response): Promise<string> => {
    try {
      const body = await response.json();
      if (typeof body.detail === 'string') return body.detail;
    } catch { /* not JSON */ }
    return 'The server rejected the request. Please try again.';
  };


  /**
   * Opens a WebSocket connection to /ws.
   * Resolves once the server sends the session_id.
   * Also handles version_update messages from the server — triggered when
   * another client performs an operation in single-backend mode.
   */
  private _openWebSocket = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      const wsUrl = `${toWebSocketUrl(this.serverUrl)}/ws`;
      this.ws = new WebSocket(wsUrl);

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
    if (!response.ok) throw new Error(await this._extractErrorMessage(response));
    return response.json();
  };

  /**
   * Public wrapper around _doFetchInfo.
   * Sets loading/error state — used after version_update and after callOperation.
   */
  fetchInfo = async (): Promise<void> => {
    this.loading = true;
    try {
      const data = await this._doFetchInfo();
      this.version = data.version;
      this.ui = data.ui ?? null;
      this.ds = data.ds ?? null;
      if (this.ui === null) {
        this.error = { code: 500, title: 'Server error', message: 'Unexpected response format. Expected ui field.' };
      }
    } catch (err) {
      this.error = { code: 500, title: 'Server Error', message: this._errorMessage(err) };
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
    try {
      const response = await fetch(`${this.serverUrl}/operation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'session-id': this.sessionId },
        body: JSON.stringify({ operation, client_version: this.version })
      });

      if (response.status === 409) {
        await this._doFetchInfo();
        this.error = { code: 409, title: 'Conflict', message: 'Action conflicts with a newer state. Please try again.' };
        return;
      }

      if (!response.ok) {
        this.error = {
          code: response.status,
          title: response.statusText,
          message: await this._extractErrorMessage(response),
        };
        return;
      }

      const data = await response.json();
      this.version = data.version ?? this.version;
      await this._doFetchInfo();
    } catch (err) {
      // Only network-level failures reach here (fetch itself threw)
      this.error = { code: 503, title: 'Network Error', message: this._errorMessage(err) };
    } finally {
      this.loading = false;
    }
  };


}

export const appContext = new AppContext();
