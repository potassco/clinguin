<script lang="ts">
  import * as Field from "$lib/components/ui/field";
  import type { ElementProps } from "$lib/frontendElement";

  let { element }: ElementProps = $props();
  const text = $derived(element.attr("text") || element.attr("label"));
</script>

<Field.Error id={element.node.id} class={element.attr("class")}>
  {text}
</Field.Error>
