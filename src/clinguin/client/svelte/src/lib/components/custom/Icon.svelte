<script lang="ts">
	import { cn } from "$lib/utils";
    import type { ElementProps } from "$lib/frontendElement";
    import * as LucideIcons from "@lucide/svelte";
    let { element }: ElementProps = $props();

    const iconName = $derived(element.attr("icon"));
    const iconSize = $derived(element.attr("icon_size") || "size-4");
    const isImagePath = $derived(
        iconName.startsWith("/") || /\.(svg|png|jpg|jpeg|webp)$/i.test(iconName)
    );
    const LucideIcon = $derived(
        !isImagePath && iconName ? (LucideIcons as any)[iconName] ?? null : null
    );
</script>

{#if isImagePath}
    <img src={iconName} alt="" class={cn(iconSize, element.attr("class"))} />
{:else if LucideIcon}
    <!-- svelte-ignore element_invalid_self_closing_tag -->
    <LucideIcon class={cn(iconSize, element.attr("class"))} />
{/if}
