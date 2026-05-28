import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import type { ClinguinNode } from "$lib/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChild<T> = T extends { child?: any } ? Omit<T, "child"> : T;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChildren<T> = T extends { children?: any } ? Omit<T, "children"> : T;
export type WithoutChildrenOrChild<T> = WithoutChildren<WithoutChild<T>>;
export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };

/** Removes surrounding quotes from a string value. */
export function unquote(value: unknown): string {
  const s = String(value ?? '');
  return s.replace(/^"(.*)"$/, '$1');
}

/** Retrieves attribute value(s) from a node by key. */
export function getAttr(node: ClinguinNode, key: string): string | undefined {
  const matches = (node.attributes ?? []).filter((a) => a?.key === key);
  if (matches.length === 0) return undefined;
  return matches.map((a) => unquote(a.value)).join(' ');
}

/** Converts an http(s) URL to its ws(s) equivalent for WebSocket connections. */
export function toWebSocketUrl(httpUrl: string): string {
  if (httpUrl.startsWith('https://')) return httpUrl.replace('https://', 'wss://');
  if (httpUrl.startsWith('http://')) return httpUrl.replace('http://', 'ws://');
  return httpUrl;
}

// Builds a map of node ID to node for quick lookup. Used in AppContext to efficiently find nodes by ID.
export function buildNodeMap(root: ClinguinNode): Map<string, ClinguinNode> {
    const map = new Map<string, ClinguinNode>();
    function traverse(node: ClinguinNode) {
        map.set(node.id, node);
        (node.children ?? []).forEach(traverse);
    }
    traverse(root);
    return map;
}

// Splits a string of comma-separated arguments while respecting nested parentheses.
export function splitAspArgs(input: string): string[] {
    const parts: string[] = [];
    let current = '';
    let depth = 0;

    for (let i = 0; i < input.length; i++) {
        const char = input[i];
        if (char === '(') depth++;
        else if (char === ')') depth--;
        else if (char === ',' && depth === 0) {
            parts.push(current.trim());
            current = '';
            continue;
        }
        current += char;
    }
    parts.push(current.trim());
    return parts;
}


// Parses an update operation string of the form "(targetId, key, value)" into its components.
export function parseUpdateOperation(op: string): { targetId: string, key: string, value: string } | null {
    if (!op.startsWith('(') || !op.endsWith(')')) return null;
    const argsString = op.slice(1, -1);
    const [targetId, key, value] = splitAspArgs(argsString);
    if (!targetId || !key || value === undefined) return null;
    return { targetId, key, value: unquote(value) };
}
