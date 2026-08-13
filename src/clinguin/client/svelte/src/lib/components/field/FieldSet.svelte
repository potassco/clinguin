<script lang="ts">
  import * as Field from "$lib/components/ui/field";
  import type { ElementProps } from "$lib/frontendElement";
  import Renderer from "$lib/Renderer.svelte";

  let { element }: ElementProps = $props();

  const legend = $derived(element.attr("legend") || element.attr("label"));
  const legendVariant = $derived(element.attr("legend_variant") || "legend"); // "legend" | "label"
  const children = $derived(element.node?.children ?? []);
</script>

<Field.Set id={element.node.id} class={element.attr("class")}>
  {#if legend}
    <Field.Legend variant={legendVariant as any}>{legend}</Field.Legend>
  {/if}
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}
</Field.Set>
