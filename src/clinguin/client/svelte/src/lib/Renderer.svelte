<!--
  Recursive rendering engine.

  Looks up the node's type in the registry and mounts the corresponding
  Svelte component. Components are responsible for rendering their own
  children by including Renderer recursively (see Container.svelte).

  If the node's type is not found in the registry, renders a fallback
  showing the unsupported type and the full node data for debugging.
-->

<script lang="ts">
  import { registry } from '$lib/registry';
  import type { ElemProps } from '$lib/useElem.svelte';

  let { node }: ElemProps = $props();

  const Component = $derived(node?.type ? registry[node.type] : null);
</script>

{#if Component}
  <Component {node} />
{:else}
  <div>
    Unsupported element type: <code>{node?.type}</code>
    <pre>{JSON.stringify(node, null, 2)}</pre>
  </div>
{/if}
