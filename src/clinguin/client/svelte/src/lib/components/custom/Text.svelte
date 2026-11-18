<script lang="ts">
  import { cn } from "$lib/utils";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";
  let { element }: ElementProps = $props();
</script>

<span
  id={element.node.id}
  {...element.get_html()}
  {...element.actions}
>
{#if element.get_icon()}
  <Renderer node={element.get_icon()!} />
{/if}
  {element.attr("label") || element.attr("text")}
</span>
