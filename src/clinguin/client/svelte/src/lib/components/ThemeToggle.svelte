<script lang="ts">
  import { toggleMode, mode } from 'mode-watcher';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';
  import * as LucideIcons from '@lucide/svelte';

  let { node }: ElemProps = $props();
  const elem = $derived(useElem(node));

  const iconDark  = $derived(elem.attr('icon_dark')  || 'Sun');
  const iconLight = $derived(elem.attr('icon_light') || 'Moon');
  const currentIcon = $derived(mode.current === 'dark' ? iconDark : iconLight);

  const IconComponent = $derived((LucideIcons as any)[currentIcon] ?? null);
</script>

<button id={node.id} onclick={toggleMode} class={elem.attr('class')} aria-label="Toggle theme">
  {#if IconComponent}
    <IconComponent class="size-4" />
  {/if}
</button>
