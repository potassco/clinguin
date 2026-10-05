<!--
  Generic component for rendering any ClinguinNode.
-->

<script lang="ts">
  import Renderer from "$lib/Renderer.svelte";
  import type { ElementProps } from "$lib/frontendElement";
  import { resolveComponent, isNativeTag } from "$lib/resolveComponent";
  import { sortedChildren } from "$lib/utils";

  let { element }: ElementProps = $props();

  const Component = $derived(resolveComponent(element.node.type));
  const isNative = $derived(
	element.node.type === "root"
		? "div"
		: !Component && isNativeTag(element.node.type)
		? element.node.type
		: null
	);
  const text = $derived(element.attr("text") || element.attr("content"));
  const children = $derived(sortedChildren(element.node.children ?? []));
</script>

{#snippet content()}
  {#each children as child (child.id)}
    <Renderer node={child} />
  {/each}

  {#if text}
    {text}
  {/if}
{/snippet}

{#if Component}
  <Component
    id={element.node.id}
    {...element.get_html()}
    {...element.actions}
  >
    {@render content()}
  </Component>
{:else if isNative}
  <svelte:element
    this={isNative}
    id={element.node.id}
    {...element.get_html()}
    {...element.actions}
  >
    {@render content()}
  </svelte:element>
{:else}
  <div>
    Unresolved component:
    <code>{element.node.type}</code>
  </div>
{/if}
