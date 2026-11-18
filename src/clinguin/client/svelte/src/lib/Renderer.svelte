<!--
  Recursive rendering engine.

  This component takes a ClinguinNode and renders it using the appropriate Svelte component.
  If the component is not found, it falls back to the Generic component.
-->

<script lang="ts">
  import { registry } from "$lib/registry";
  import { FrontendElement } from "$lib/frontendElement";
  import type { ClinguinNode } from "$lib/types";
  import Generic from "./components/Generic.svelte";

  export interface NodeProps {
    node: ClinguinNode;
  }
  let { node }: NodeProps = $props();
  let elem = $derived(new FrontendElement(node));
  // svelte-ignore state_referenced_locally
  //console.log("Rendering node:", elem);

  //let elem_order = $derived(elem.attr("order"));

  const Component = $derived(elem.node?.type ? (registry[elem.node.type] ?? Generic) : null);
</script>

{#if Component}
		<Component element={elem} />
{:else}
  <div>
    Unsupported element type: <code>{node?.type}</code>
    <pre>{JSON.stringify(node, null, 2)}</pre>
  </div>
{/if}
