<script lang="ts">
  import { cn } from '$lib/utils';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';

  let { node }: ElemProps = $props();

  const elem = $derived(useElem(node));
</script>

<span class={cn(elem.attr('class'))} {...elem.actions}>
  {elem.attr('label') || elem.attr('text')}
</span>
