<script lang="ts">
  import * as Field from "$lib/components/ui/field";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();

  const label = $derived(element.attr("text") || element.attr("label"));
  const forId = $derived(element.attr("for"));
  const icon = $derived(element.get_icon());
  const children = $derived(element.node?.children ?? []);
</script>

<Field.Label id={element.node.id} for={forId || undefined} class={element.attr("class")}>
  {#if icon}
    <Renderer node={icon} />
  {/if}
  {label}
  {#each children as child (child.id)}
    {#if child.type !== "icon"}
      <Renderer node={child} />
    {/if}
  {/each}
</Field.Label>
