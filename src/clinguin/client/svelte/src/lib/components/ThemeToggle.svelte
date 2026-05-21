<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { toggleMode, mode } from "mode-watcher";
  import * as LucideIcons from "@lucide/svelte";

  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();

  const iconDark = $derived(element.attr("icon_dark") || "Sun");
  const iconLight = $derived(element.attr("icon_light") || "Moon");
  const currentIcon = $derived(mode.current === "dark" ? iconDark : iconLight);
  const variant = $derived(element.attr("variant") || "default"); // support 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link'

  const size = $derived(element.attr("size") || "default");

  const IconComponent = $derived((LucideIcons as any)[currentIcon] ?? null);
</script>

<Button
  id={element.node.id}
  onclick={toggleMode}
  class={element.attr("class")}
  variant={variant as any}
  size={size as any}
  aria-label="Toggle theme"
>
  {#if IconComponent}
    <IconComponent class="size-4" />
  {/if}
</Button>
