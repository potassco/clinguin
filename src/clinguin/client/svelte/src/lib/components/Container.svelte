<script lang="ts">
  import { useElem } from '$lib/useElem.svelte';
  import { cn } from '$lib/utils';
  import type { ElemProps } from '$lib/useElem.svelte';
  import Renderer from '$lib/Renderer.svelte';

  let { node }: ElemProps = $props();

  const elem = $derived(useElem(node));
  const children = $derived(node?.children ?? []);
</script>

<div class={cn(elem.attr('class'))} {...elem.actions}>
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}
</div>
