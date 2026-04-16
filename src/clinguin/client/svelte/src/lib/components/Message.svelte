<script lang="ts">
  import { toast } from 'svelte-sonner';
  import { useElem } from '$lib/useElem.svelte';
  import type { ElemProps } from '$lib/useElem.svelte';
  import { onMount } from 'svelte';

  let { node }: ElemProps = $props();

  onMount(() => {
    const elem = useElem(node);
    const title = elem.attr('title');
    const message = elem.attr('message');
    const type = elem.attr('type') || 'info';

    switch (type) {
      case 'success':
        toast.success(title, { description: message });
        break;
      case 'danger':
        toast.error(title, { description: message });
        break;
      case 'warning':
        toast.warning(title, { description: message });
        break;
      default:
        toast.info(title, { description: message });
    }
  });
</script>
