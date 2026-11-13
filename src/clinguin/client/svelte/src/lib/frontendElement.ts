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
import type { HTMLAttributes } from 'svelte/elements';
import { toPascalCase } from '$lib/resolveComponent';

export interface ElementProps {
	element: FrontendElement;
}


const CLINGUIN_ATTRS = new Set([
	'order',
	'text',
	'content'
]);


export class FrontendElement {
	actions = {};

	constructor(public node: ClinguinNode) {
		this.node = node;

		/**
		 * Maps when/4 entries from the node to a DOM-ready event handler map.
		 * For example, when(my_button, click, call, next_solution) becomes:
		 * { onClick: () => appContext.handleWhen(...) }
		 */

		const whens = this.node.when ?? [];
		const events = [...new Set(whens.map((w) => w.event))];

		this.actions = Object.fromEntries(
			events.map((event) => [
				event.includes('_') ? `on${toPascalCase(event)}` : `on${event}`,
				async (arg: unknown) => {
					const e = arg instanceof Event ? arg : undefined;
					const value = e ? undefined : arg;
					if (e?.type === 'submit') {
						e.preventDefault();
						await appContext.addFormContext(e.target as HTMLFormElement, (e as SubmitEvent).submitter);
					}
					for (const w of whens.filter((w) => w.event === event).sort((a, b) => Number(a.action === 'call') - Number(b.action === 'call'))) {
						await appContext.handleWhen(w, e, value);
					}
				}
			])

		);
	}
	/**
	 * Reads an attribute value from the node by key.
	 * Returns fallback (default: '') if the key is not found.
	 */
	attr(key: string, fallback = ''): string {
		return getAttr(this.node, key) ?? fallback;
	}

	get_icon(): ClinguinNode | null {
		// Find icon in the children
		// if there is no icon then return null
		// {#if element.get_icon()}<Renderer node={element.get_icon()} />{/if}

		return this.node.children?.find((c) => c.type === 'icon') ?? null;
	}

	get_html<T extends HTMLAttributes<HTMLElement>>(...keys: (keyof T)[]): Partial<T> {
		// For each key in HTMLAttributes, if we have it as an attribute in the element then return
		// Some error handling that if something is set but is invalid
		// Start getting all of them with the HTMLElement
		const result: Partial<T> = {};
		const attrs = this.node.attributes ?? [];
		const keysToCheck = keys.length > 0 ? keys
		: attrs.map((a) => a.key as keyof T).filter((k) => !CLINGUIN_ATTRS.has(k as string));

		for (const key of keysToCheck) {
			const value = getAttr(this.node, key as string);
			if (value !== undefined) {
				(result as any)[key] = value === 'true' ? true : value === 'false' ? false : value; // Convert "true"/"false" to boolean
			}
		}
		return result;
	}
}
