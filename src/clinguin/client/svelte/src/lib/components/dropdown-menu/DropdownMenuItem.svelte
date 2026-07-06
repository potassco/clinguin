<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import Renderer from "$lib/Renderer.svelte";

	let { element }: ElementProps = $props();

	const label = $derived(element.attr("text") || element.attr("label"));
	const variant = $derived(element.attr("variant") || "default"); // variant?: "default" | "destructive";
	const inset = $derived(element.attr("inset") === "true"); // inset?: boolean;

	const checkedAttr = $derived(element.attr("checked", ""));
	const isCheckbox = $derived(checkedAttr !== "");
	const checked = $derived(checkedAttr === "true");
</script>

{#snippet itemContent()}
	{#if element.get_icon()}
		<Renderer node={element.get_icon()!} />
	{/if}
	{label}
{/snippet}

{#if isCheckbox}
	<DropdownMenu.CheckboxItem
		id={element.node.id ?? undefined}
		checked={checked}
		class={element.attr("class")}
		{...element.actions}
	>
		{@render itemContent()}
	</DropdownMenu.CheckboxItem>
{:else}
	<DropdownMenu.Item
		id={element.node.id ?? undefined}
		variant={variant as any}
		inset={inset}
		class={element.attr("class")}
		{...element.actions}
	>
		{@render itemContent()}
	</DropdownMenu.Item>
{/if}
