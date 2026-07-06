<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import { getAttr } from "$lib/utils";
	import Renderer from "$lib/Renderer.svelte";

	let { element }: ElementProps = $props();

	const label = $derived(element.attr("label"));
	const children = $derived(element.node?.children ?? []);
	const sortedChildren = $derived(
		[...children].sort((a, b) => Number(getAttr(a, "order") ?? 0) - Number(getAttr(b, "order") ?? 0))
	);
</script>

<DropdownMenu.Separator />
<DropdownMenu.Group id={element.node.id}>
	{#if label}
		<DropdownMenu.Label>{label}</DropdownMenu.Label>
	{/if}
	{#each sortedChildren as child (child.id)}
		<Renderer node={child} />
	{/each}
</DropdownMenu.Group>
