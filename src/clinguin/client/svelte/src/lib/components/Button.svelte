<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import FrontendElement from '$lib/frontendElement';
  import type { ElemProps } from '$lib/frontendElement';

  let { node }: ElemProps = $props();

  const elem = $derived(FrontendElement(node));
  const label = $derived(elem.attr('text') || elem.attr('label'));
  const variant = $derived(elem.attr('variant') || 'default'); // support 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link'
  const size = $derived(elem.attr('size') || 'default');
</script>

<Button
  id={node.id}
  style={elem.style}
  variant={variant as any}
  size={size as any}
  class={elem.attr('class')}
  {...elem.actions}
>
  {#if elem.icon}
    <elem.icon class="size-4" />
  {/if}
  {label}
</Button>
