<script lang="ts">
  import { cn } from "$lib/utils";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();
  console.log("Container element:", element);
  const children = $derived(element.node?.children ?? []);
</script>

<div
  id={element.node.id}
  class={cn(element.attr("class"))}
  style={element.style}
  {...element.actions}
>
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}
</div>
