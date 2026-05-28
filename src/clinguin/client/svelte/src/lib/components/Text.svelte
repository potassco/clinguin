<script lang="ts">
  import { cn } from "$lib/utils";
  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();
</script>

<span
  id={element.node.id}
  class={cn(element.attr("class"))}
  {...element.actions}
  hidden={element.hidden}
>
{#if element.iconSrc}
  <img src={element.iconSrc} alt="" class={element.iconSize}/>
{:else if element.icon}
  <element.icon class={element.iconSize} />
{/if}
  {element.attr("label") || element.attr("text")}
</span>
