<script lang="ts">
  import { Input } from "$lib/components/ui/input";
  import type { ElementProps } from "$lib/frontendElement";

  let { element }: ElementProps = $props();

  // nothing is sent anywhere until `context` is wired.

  const type = $derived(element.attr("type") || "text");
  const placeholder = $derived(element.attr("placeholder"));
  const disabled = $derived(element.attr("disabled") === "true");
  const value = $derived(element.attr("value"));
</script>

<Input
  id={element.node.id}
  type={type as any}
  placeholder={placeholder}
  disabled={disabled}
  value={value}
  class={element.attr("class")}
  {...element.actions}
/>
