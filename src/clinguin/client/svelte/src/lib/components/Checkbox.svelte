<script lang="ts">
  import { Checkbox } from "$lib/components/ui/checkbox";
  import type { ElementProps } from "$lib/frontendElement";

  let { element }: ElementProps = $props();

  const disabled = $derived(element.attr("disabled") === "true");
  const checked = $derived(element.attr("checked") === "true");
  const indeterminate = $derived(element.attr("indeterminate") === "true");
</script>

<Checkbox
  id={element.node.id}
  {...element.actions}
  {disabled}
  {checked}
  {indeterminate}
  class={element.attr("class")}
/>
