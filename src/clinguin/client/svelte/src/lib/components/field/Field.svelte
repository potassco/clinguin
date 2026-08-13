<script lang="ts">
  import * as Field from "$lib/components/ui/field";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();

  const orientation = $derived(element.attr("orientation") || "vertical"); // "vertical" | "horizontal" | "responsive"
  const invalid = $derived(element.attr("invalid") === "true");
  const children = $derived(element.node?.children ?? []);
</script>

<Field.Field
  id={element.node.id}
  orientation={orientation as any}
  data-invalid={invalid}
  class={element.attr("class")}
  {...element.actions}
>
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}
</Field.Field>
