<script lang="ts">
  // General
  import { Button } from "$lib/components/ui/button";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();

  // Custom/ShadCn component attributes
  const label = $derived(element.attr("text") || element.attr("label"));
  const variant = $derived(element.attr("variant") || "default"); // support 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link'
  const size = $derived(element.attr("size") || "default");
</script>

<Button
  id={element.node.id}
  {...element.get_html()}
  {...element.actions}
  variant={variant as any}
  size={size as any}
>
  {#if element.get_icon()}
  	<Renderer node={element.get_icon()!} />
  {/if}
  {label}
</Button>
