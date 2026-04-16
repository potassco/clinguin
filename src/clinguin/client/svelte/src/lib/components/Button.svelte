<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';

  let { node }: ElemProps = $props();

  const elem = $derived(useElem(node));
  const label = $derived(elem.attr('label') || elem.attr('text'));
  const variant = $derived(elem.attr('variant') || 'default'); // support 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link'
  const size = $derived(elem.attr('size') || 'default');
</script>

<Button
  variant={variant as any}
  size={size as any}
  class={elem.attr('class')}
  {...elem.actions}
>
  {label}
</Button>
