<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import Renderer from "$lib/Renderer.svelte";

	let { element }: ElementProps = $props();

	const value = $derived(element.attr("value"));
	const children = $derived(element.node?.children ?? []);
</script>

<DropdownMenu.RadioGroup value={value}>
	{#each children as child (child.id)}
		<Renderer node={child} />
	{/each}
</DropdownMenu.RadioGroup>
