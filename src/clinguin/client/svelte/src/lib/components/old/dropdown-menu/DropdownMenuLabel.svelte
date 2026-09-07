<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";

	let { element }: ElementProps = $props();

	const label = $derived(element.attr("text") || element.attr("label"));
	const inset = $derived(element.attr("inset") === "true");
</script>

<DropdownMenu.Label
	id={element.node.id}
	inset={inset}
	class={element.attr("class")}
>
	{label}
</DropdownMenu.Label>
