<!--
  Recursive rendering engine.

  Looks up the node's type in the registry and mounts the corresponding
  Svelte component. Components are responsible for rendering their own
  children by including Renderer recursively (see Container.svelte).

  If the node's type is not found in the registry, renders a fallback
  showing the unsupported type and the full node data for debugging.
-->

<script lang="ts">
  import { registry } from "$lib/registry";
  import { FrontendElement } from "$lib/frontendElement";
  import type { ClinguinNode } from "$lib/types";

  export interface NodeProps {
    node: ClinguinNode;
  }
  let { node }: NodeProps = $props();
  function toFrontendElement(node: ClinguinNode): FrontendElement {
    return new FrontendElement(node);
  }
  let elem = $derived(toFrontendElement(node));
  console.log("Rendering node:", elem);

  const Component = $derived(elem.node?.type ? registry[elem.node.type] : null);
</script>

{#if Component}
  <Component element={elem} />
{:else}
  <div>
    Unsupported element type: <code>{node?.type}</code>
    <pre>{JSON.stringify(node, null, 2)}</pre>
  </div>
{/if}
