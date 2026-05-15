<script lang="ts">
  import { cn } from '$lib/utils';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';

  let { node }: ElemProps = $props();

  const elem = $derived(useElem(node));
</script>

<span id={node.id} class={cn(elem.attr('class'))} {...elem.actions}>
  {#if elem.icon}
    <elem.icon class="size-4" />
  {/if}
  {elem.attr('label') || elem.attr('text')}
</span>
