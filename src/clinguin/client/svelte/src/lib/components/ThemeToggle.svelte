<script lang="ts">
  import { toggleMode, mode } from "mode-watcher";
  import * as LucideIcons from "@lucide/svelte";

  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();

  const iconDark = $derived(element.attr("icon_dark") || "Sun");
  const iconLight = $derived(element.attr("icon_light") || "Moon");
  const currentIcon = $derived(mode.current === "dark" ? iconDark : iconLight);

  const IconComponent = $derived((LucideIcons as any)[currentIcon] ?? null);
</script>

<button
  id={element.node.id}
  onclick={toggleMode}
  class={element.attr("class")}
  aria-label="Toggle theme"
>
  {#if IconComponent}
    <IconComponent class="size-4" />
  {/if}
</button>
