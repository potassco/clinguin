<script lang="ts">
  import { appContext } from "$lib/context.svelte";
  import { Badge } from "$lib/components/ui/badge";
  import { Label } from "$lib/components/ui/label";
  import { Switch } from "$lib/components/ui/switch";
  import type { ClinguinNode } from "$lib/types";

  const HIGHLIGHT = "data-clinguin-inspected";
  const HIGHLIGHT_PARENT = "data-clinguin-inspected-parent";

  let selectedId = $state<string | null>(null);
  // When off, clicks reach the app again; the selected node keeps updating live.
  let active = $state(true);

  // Map of all nodes in the UI, indexed by their ID.
  const nodes = $derived.by(() => {
    const index = new Map<string, ClinguinNode>();
    const add = (node: ClinguinNode) => {
      index.set(node.id, node);
      node.children?.forEach(add);
    };
    if (appContext.ui) add(appContext.ui);
    return index;
  });

  // Selected node preceded by at most two ancestors (the root is its own parent).
  const path = $derived.by(() => {
    const result: ClinguinNode[] = [];
    let node = selectedId ? nodes.get(selectedId) : undefined;
    while (node && result.length < 3) {
      result.unshift(node);
      node = node.parent === node.id ? undefined : nodes.get(node.parent);
    }
    return result;
  });

  // Highlight the selected node and its ancestors in the UI.
  $effect(() => {
    const highlighted: Element[] = [];
    const visited = new Set<string>();
    let mainNode = selectedId ? nodes.get(selectedId) : undefined;
    let node = mainNode;
    while (node && !visited.has(node.id)) {
      visited.add(node.id);
      const element = document.getElementById(node.id);
      if (element) {
        if (node === mainNode) {
          element.setAttribute(HIGHLIGHT, "");
        } else {
          element.setAttribute(HIGHLIGHT_PARENT, "ancestor");
        }
        highlighted.push(element);
      }
      node = node.parent === node.id ? undefined : nodes.get(node.parent);
    }
    return () =>
      highlighted.forEach((element) => {
        element.removeAttribute(HIGHLIGHT);
        element.removeAttribute(HIGHLIGHT_PARENT);
      });
  });

  // Inspect a node when the user clicks on it in the UI.
  const inspect = (event: MouseEvent) => {
    if (!active || !(event.target instanceof Element)) return;
    if (event.target.closest("[data-clinguin-inspector]")) return;

    const element = event
      .composedPath()
      .find(
        (item): item is Element =>
          item instanceof Element && nodes.has(item.id),
      );
    if (!element) return;

    // Inspect mode consumes clicks instead of executing UI actions.
    event.preventDefault();
    event.stopPropagation();
    selectedId = element.id;
  };
</script>

<svelte:document onclickcapture={inspect} />

{#snippet section(title: string, lines: string[] = [])}
  {#if lines.length}
    <div class="mt-2 border-t border-border pt-2">
      <div class="mb-1 font-sans font-medium text-muted-foreground">
        {title}
      </div>
      {#each lines as line}<div>{line}</div>{/each}
    </div>
  {/if}
{/snippet}

<aside
  data-clinguin-inspector
  class="sticky top-0 h-screen w-80 shrink-0 overflow-y-auto border-l border-border bg-muted/30"
>
  <header
    class="sticky top-0 flex items-center justify-between border-b border-border bg-background px-4 py-3"
  >
    <h2 class="text-sm font-semibold">Inspector</h2>
    <div class="flex items-center gap-2">
      <Label for="clinguin-inspect-mode" class="text-xs text-muted-foreground"
        >Inspect mode</Label
      >
      <Switch id="clinguin-inspect-mode" bind:checked={active} />
    </div>
  </header>

  <div class="space-y-2 p-4 font-mono text-xs wrap-anywhere">
    {#each path as node, depth (node.id)}
      <details
        open={depth === path.length - 1}
        class="rounded-lg border border-border bg-background shadow-sm"
        style:margin-left="{depth * 0.75}rem"
      >
        <summary class="cursor-pointer px-3 py-2 font-semibold">
          {node.id}
          <Badge variant="outline" class="ml-1 align-middle font-normal"
            >{node.type}</Badge
          >
        </summary>

        <div class="border-t border-border px-3 py-2">
          <div class="text-muted-foreground">parent: {node.parent}</div>
          {@render section(
            "Attributes",
            node.attributes?.map((a) => `${a.key} = ${a.value}`),
          )}
          {@render section(
            "Actions",
            node.when?.map((w) =>
              [w.event, w.action, w.operation].filter(Boolean).join(" → "),
            ),
          )}
        </div>
      </details>
    {:else}
      <p class="font-sans text-sm text-muted-foreground">
        {active
          ? "Click a UI element to inspect it."
          : "Turn on inspect mode to select elements."}
      </p>
    {/each}
  </div>
</aside>
