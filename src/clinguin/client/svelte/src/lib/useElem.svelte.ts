/**
 * Shared composable for all Clinguin UI components.
 *
 * Every component receives a ClinguinNode and uses useElem to extract:
 *   - attr(key): reads an attribute value from the node by key
 *   - actions: a DOM-ready event handler map built from the node's when/4 entries
 *
 */

import { getAttr } from '$lib/utils';
import type { ClinguinNode } from '$lib/context.svelte';
import { appContext } from '$lib/context.svelte';
import * as LucideIcons from '@lucide/svelte';

/** Base prop interface for all Clinguin components. */
export interface ElemProps {
  node: ClinguinNode;
}

export function useElem(node: ClinguinNode) {
  /**
   * Reads an attribute value from the node by key.
   * Returns fallback (default: '') if the key is not found.
   */
  function attr(key: string, fallback = ''): string {
    return getAttr(node, key) ?? fallback;
  }

  /**
   * Maps when/4 entries from the node to a DOM-ready event handler map.
   * For example, when(my_button, click, call, next_solution) becomes:
   * { onClick: () => appContext.handleWhen(...) }
   */
  const actions = Object.fromEntries(
    (node.when ?? []).map((w) => [
      `on${w.event}`,
      () => appContext.handleWhen(w)
    ])
  );

  const iconName = getAttr(node, 'icon');
  const icon = iconName ? (LucideIcons as any)[iconName] ?? null : null;

  const orderVal = attr('order');
  const style = orderVal ? `order: ${orderVal}` : undefined;

  return { attr, actions, icon, style };
}
