/**
 * Shared composable for all Clinguin UI components.
 *
 * Every component receives a ClinguinNode and uses FrontendElement to extract:
 *   - attr(key): reads an attribute value from the node by key
 *   - actions: a DOM-ready event handler map built from the node's when/4 entries
 *
 */

import { getAttr } from '$lib/utils';
import type { ClinguinNode, ClinguinWhen } from '$lib/types';
import { appContext } from '$lib/context.svelte';
import * as LucideIcons from '@lucide/svelte';


export interface ElementProps {
	element: FrontendElement;
}

export class FrontendElement {
	actions = {};
	icon: any = null
	iconName: string | undefined = undefined;
	iconSrc: string | null = null;
	iconSize: string | undefined = undefined;
	style: string | undefined = undefined;
	orderVal: string | undefined = undefined;
	constructor(public node: ClinguinNode) {
		this.node = node;

		/**
		 * Maps when/4 entries from the node to a DOM-ready event handler map.
		 * For example, when(my_button, click, call, next_solution) becomes:
		 * { onClick: () => appContext.handleWhen(...) }
		 */

		const grouped = new Map<string, ClinguinWhen[]>();
		(node.when ?? []).forEach((w) => {
			const eventKey = `on${w.event}`;
			if (!grouped.has(eventKey)) grouped.set(eventKey, []);
			grouped.get(eventKey)!.push(w);
		});

		const order: Record<string, number> = {update: 0, context: 1, call: 2};
		this.actions = Object.fromEntries(
			Array.from(grouped.entries()).map(([eventKey, whens]) => {
				whens.sort((a, b) => order[a.action] - order[b.action]);
				return [eventKey, async () => {
					for (const when of whens) {
						await appContext.handleWhen(when);
					}
				}];
			})
		);

		this.iconName = getAttr(this.node, 'icon');
		const isImagePath = this.iconName &&
			(this.iconName.startsWith('/') || /\.(svg|png|jpg|jpeg|webp)$/i.test(this.iconName));

		this.iconSrc = isImagePath ? (this.iconName ?? null) : null;
		this.icon = !isImagePath && this.iconName
			? (LucideIcons as any)[this.iconName] ?? null
			: null;

		this.iconSize = this.attr('icon_size') || 'size-4';
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

	get hidden(): boolean {
		return this.attr('visibility') === 'hidden';
	}
}
