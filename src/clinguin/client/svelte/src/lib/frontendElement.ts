/**
 * Shared composable for all Clinguin UI components.
 *
 * Every component receives a ClinguinNode and uses FrontendElement to extract:
 *   - attr(key): reads an attribute value from the node by key
 *   - actions: a DOM-ready event handler map built from the node's when/4 entries
 *
 */

import { getAttr } from '$lib/utils';
import type { ClinguinNode } from '$lib/types';
import { appContext } from '$lib/context.svelte';
import * as LucideIcons from '@lucide/svelte';
import type { HTMLAttributes } from 'svelte/elements';

export interface ElementProps {
	element: FrontendElement;
}

export class FrontendElement {
	actions = {};
	// icon: any = null
	// iconName: string | undefined = undefined;
	// iconSrc: string | null = null;
	// iconSize: string | undefined = undefined;
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
		// this.iconName = getAttr(this.node, 'icon');
		// const isImagePath = this.iconName &&
		// 	(this.iconName.startsWith('/') || /\.(svg|png|jpg|jpeg|webp)$/i.test(this.iconName));

		// this.iconSrc = isImagePath ? (this.iconName ?? null) : null;
		// this.icon = !isImagePath && this.iconName
		// 	? (LucideIcons as any)[this.iconName] ?? null
		// 	: null;

		// this.iconSize = this.attr('icon_size') || 'size-4';
		// this.orderVal = this.attr('order');
		// this.style = this.orderVal ? `order: ${this.orderVal}` : undefined;
	}
	/**
	 * Reads an attribute value from the node by key.
	 * Returns fallback (default: '') if the key is not found.
	 */
	attr(key: string, fallback = ''): string {
		return getAttr(this.node, key) ?? fallback;
	}

	get_icon() {
		// Find icon in the children
		// if there is no icon then return null
		// {#if element.get_icon()}<Renderer node={element.get_icon()} />{/if}
	}

	get_html<T extends HTMLAttributes<HTMLElement>>(...keys: (keyof T)[]): Partial<T> {
		// For each key in HTMLAttributes, if we have it as an attribute in the element then return
		// Some error handling that if something is set but is invalid
		// Start getting all of them with the HTMLElement
		HTMLAttributes<HTMLDivElement>
		return getAttr(this.node, key)
	}
}
