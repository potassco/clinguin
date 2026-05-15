<script lang="ts">
  import { cn } from "$lib/utils";
  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();
</script>

<span
  id={element.node.id}
  class={cn(element.attr("class"))}
  {...element.actions}
>
  {#if element.icon}
    <element.icon class="size-4" />
  {/if}
  {element.attr("label") || element.attr("text")}
</span>
