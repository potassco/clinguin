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
  const match = s.match(/^"(.*)"$/s);
  if (!match) return s;
  return match[1].replace(/\\(["\\n])/g, (_, c) => (c === 'n' ? '\n' : c));
}

/** Converts a raw DOM value into clingo's text form, based on the input type. */
export function toAspTerm(value: string, type = 'text'): string {
  if (value === '') return '';
  if (type === 'number' || type === 'range') return String(Number(value));
  if (type === 'checkbox') return 'true';
  if (['select-one', 'radio'].includes(type)) return value;
  return JSON.stringify(value);
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

/** Parses an update operation string of the form "(id,key,value)" into its components. */
export function parseUpdateOperation(operation: string): { id: string; key: string; value: string } | null {
  const match = operation.trim().match(/^\((.+),(.+),(.+)\)$/);
  if (!match) return null;
  return {
    id: match[1].trim(),
    key: match[2].trim(),
    value: match[3].trim(),
  };
}


/** Sorts a list of ClinguinNode children by their "order" attribute, defaulting to 0 if not present. */
export function sortedChildren(children: ClinguinNode[]): ClinguinNode[] {
  return [...children].sort((a, b) => {
    const oa = Number(getAttr(a, "order")) || 0;
    const ob = Number(getAttr(b, "order")) || 0;
    return oa - ob;
  });
}


export function aspArgumentSplitter(aspArguments: string): string[] {
  const result: string[] = [];
  let current = '';
  let bracketLevel = 0;
  let inString = false;

  for (let i = 0; i < aspArguments.length; i++) {
    const c = aspArguments.charAt(i);
    if (c === '"' && aspArguments.charAt(i - 1) !== '\\') inString = !inString;
    if (!inString && c === '(') bracketLevel++;
    if (!inString && c === ')') bracketLevel--;
    if (!inString && c === ',' && bracketLevel === 0) {
      result.push(current.trim());
      current = '';
    } else {
      current += c;
    }
  }
  result.push(current.trim());
  return result;
}
