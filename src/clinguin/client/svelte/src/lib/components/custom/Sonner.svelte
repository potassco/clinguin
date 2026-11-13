<script lang="ts">
  import { toast } from "svelte-sonner";
  import { onMount } from "svelte";

  import type { ElementProps } from "$lib/frontendElement";
  let { element }: ElementProps = $props();

  onMount(() => {
    const title = element.attr("title");
    const description = element.attr("description") || "";
    const type = element.attr("type") || "info";

    switch (type) {
      case "success":
        toast.success(title, { description: description });
        break;
      case "danger":
        toast.error(title, { description: description });
        break;
      case "warning":
        toast.warning(title, { description: description });
        break;
      default:
        toast.info(title, { description: description });
    }
  });
</script>
