<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import { FrontendElement } from "$lib/frontendElement";
	import DropdownMenuRoot from "./DropdownMenu.svelte";
	import Renderer from "$lib/Renderer.svelte";
	import { getAttr } from "$lib/utils";

	let { element, sub = false }: ElementProps & { sub?: boolean } = $props();

	const align = $derived(element.attr("align") || "start"); // "start" | "center" | "end"
	const sideOffset = $derived(Number(element.attr("side_offset")) || 4);
	const children = $derived(element.node?.children ?? []);
	const sortedChildren = $derived(
		[...children].sort((a, b) => Number(getAttr(a, "order")) - Number(getAttr(b, "order")))
	);
</script>

{#snippet items()}
	{#each sortedChildren as child (child.id)}
		{#if child.type === 'dropdown_menu'}
			<DropdownMenuRoot element={new FrontendElement(child)} sub={true} />
		{:else}
			<Renderer node={child} />
		{/if}
	{/each}
{/snippet}

{#if sub}
	<DropdownMenu.SubContent
		id={element.node.id}
		class={element.attr("class")}
	>
		{@render items()}
	</DropdownMenu.SubContent>
{:else}
	<DropdownMenu.Content
		id={element.node.id}
		align={align as any}
		sideOffset={sideOffset}
		class={element.attr("class")}
	>
		{@render items()}
	</DropdownMenu.Content>
{/if}
