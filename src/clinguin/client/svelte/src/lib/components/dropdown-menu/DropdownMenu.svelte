<script lang="ts">
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
	import type { ElementProps } from "$lib/frontendElement";
	import { FrontendElement } from "$lib/frontendElement";
	import DropdownMenuContent from "./DropdownMenuContent.svelte";
	import Renderer from "$lib/Renderer.svelte";

	let { element, sub = false }: ElementProps & { sub?: boolean } = $props();

	const trigger = $derived(element.attr("text") || element.attr("label"));
	const icon = $derived(element.get_icon());

	const contentNode = $derived(
		element.node?.children?.find((c) => c.type === "dropdown_menu_content") ?? null
	);
	const contentElem = $derived(contentNode ? new FrontendElement(contentNode) : null);
</script>

{#snippet triggerContent()}
	{#if icon}
		<Renderer node={icon} />
	{/if}
	{trigger}
{/snippet}

{#if sub}
	<DropdownMenu.Sub>
		<DropdownMenu.SubTrigger
			id={element.node.id}
			class={element.attr("class")}
			{...element.actions}
		>
			{@render triggerContent()}
		</DropdownMenu.SubTrigger>
		{#if contentElem}
			<DropdownMenuContent element={contentElem} sub={true} />
		{/if}
	</DropdownMenu.Sub>
{:else}
	<DropdownMenu.Root>
		<DropdownMenu.Trigger>
			<button
				id={element.node.id}
				{...element.get_html()}
				{...element.actions}
			>
				{@render triggerContent()}
			</button>
		</DropdownMenu.Trigger>
		{#if contentElem}
			<DropdownMenuContent element={contentElem} sub={false} />
		{/if}
	</DropdownMenu.Root>
{/if}
