import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import type { ClinguinNode } from "$lib/context.svelte";

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
  if (httpUrl.startsWith('http://'))  return httpUrl.replace('http://',  'ws://');
  return httpUrl;
}
