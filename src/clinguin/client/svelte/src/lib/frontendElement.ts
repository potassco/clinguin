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

class FrontendElement{
	actions = {};
	icon: any = null
	iconName: string | undefined = undefined;
	style: string | undefined = undefined;
	orderVal: string | undefined = undefined;
	constructor(public node: ClinguinNode) {
		this.node = node;

		/**
		 * Maps when/4 entries from the node to a DOM-ready event handler map.
		 * For example, when(my_button, click, call, next_solution) becomes:
		 * { onClick: () => appContext.handleWhen(...) }
		 */

		this.actions = Object.fromEntries(
		(this.node.when ?? []).map((w) => [
		`on${w.event}`,
		() => appContext.handleWhen(w)
		])
	);
		this.iconName = getAttr(this.node, 'icon');
  		this.icon = this.iconName ? (LucideIcons as any)[this.
			iconName] ?? null : null;

		this.orderVal = this.attr('order');
		this.style = this.orderVal ? `order: ${this.orderVal}` : undefined;
	}
  /**
   * Reads an attribute value from the node by key.
   * Returns fallback (default: '') if the key is not found.
   */
  	attr(key: string, fallback = ''): string {
    	return getAttr(this.node, key) ?? fallback;
 	}
}
