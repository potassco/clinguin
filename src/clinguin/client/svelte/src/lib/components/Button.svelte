<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();

  const label = $derived(element.attr("text") || element.attr("label"));
  const variant = $derived(element.attr("variant") || "default"); // support 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link'
  const size = $derived(element.attr("size") || "default");
</script>

<Button
  id={element.node.id}
  style={element.style}
  variant={variant as any}
  size={size as any}
  class={element.attr("class")}
  {...element.actions}
>
  {#if element.icon}
    <element.icon class="size-4" />
  {/if}
  {label}
</Button>
