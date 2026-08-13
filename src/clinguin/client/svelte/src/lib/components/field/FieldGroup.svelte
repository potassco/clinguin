<script lang="ts">
  import * as Field from "$lib/components/ui/field";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();
  const children = $derived(element.node?.children ?? []);
</script>

<Field.Group id={element.node.id} class={element.attr("class")}>
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}
</Field.Group>
