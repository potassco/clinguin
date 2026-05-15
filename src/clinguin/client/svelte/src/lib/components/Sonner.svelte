<script lang="ts">
  import { toast } from "svelte-sonner";
  import { onMount } from "svelte";

  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();

  onMount(() => {
    const title = element.attr("title");
    const sonner = element.attr("sonner");
    const type = element.attr("type") || "info";

    switch (type) {
      case "success":
        toast.success(title, { description: sonner });
        break;
      case "danger":
        toast.error(title, { description: sonner });
        break;
      case "warning":
        toast.warning(title, { description: sonner });
        break;
      default:
        toast.info(title, { description: sonner });
    }
  });
</script>
