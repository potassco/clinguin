<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import Renderer from "$lib/Renderer.svelte";

	let { element }: ElementProps = $props();

	const label = $derived(element.attr("label") || element.attr("text"));
	const value = $derived(element.attr("value"));
</script>

<DropdownMenu.RadioItem
	id={element.node.id}
	value={value}
	class={element.attr("class")}
	{...element.actions}
>
	{#if element.get_icon()}
		<Renderer node={element.get_icon()!} />
	{/if}

	{label}
</DropdownMenu.RadioItem>
