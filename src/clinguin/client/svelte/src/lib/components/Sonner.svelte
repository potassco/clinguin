<script lang="ts">
  import { toast } from 'svelte-sonner';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';
  import { onMount } from 'svelte';

  let { node }: ElemProps = $props();

  onMount(() => {
    const elem = useElem(node);
    const title = elem.attr('title');
    const sonner = elem.attr('sonner');
    const type = elem.attr('type') || 'info';

    switch (type) {
      case 'success':
        toast.success(title, { description: sonner });
        break;
      case 'danger':
        toast.error(title, { description: sonner });
        break;
      case 'warning':
        toast.warning(title, { description: sonner });
        break;
      default:
        toast.info(title, { description: sonner });
    }
  });
</script>
