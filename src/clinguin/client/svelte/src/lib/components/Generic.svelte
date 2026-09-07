<!--
  Generic component for rendering any ClinguinNode.
-->

<script lang="ts">
  import Renderer from "$lib/Renderer.svelte";
  import type { ElementProps } from "$lib/frontendElement";
  import { resolveComponent } from "$lib/resolveComponent";
  import { sortedChildren } from "$lib/utils";

  let { element }: ElementProps = $props();

  const Component = $derived(resolveComponent(element.node.type));
  const text = $derived(element.attr("text") || element.attr("content"));
  const children = $derived(sortedChildren(element.node.children ?? []));
</script>

{#if Component}
  <Component
    id={element.node.id}
    {...element.get_html()}
    {...element.actions}
  >
    {#each children as child (child.id)}
      <Renderer node={child} />
    {/each}

    {#if text}
      {text}
    {/if}
  </Component>
{:else}
  <div>
    Unresolved component:
    <code>{element.node.type}</code>
  </div>
{/if}
