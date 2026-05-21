<script lang="ts">
  import { onMount } from "svelte";
  import { appContext } from "$lib/context.svelte";
  import { ModeWatcher } from "mode-watcher";
  import "../app.css";

  let { children } = $props();

  onMount(() => {
    appContext.connect();
  });
</script>

<ModeWatcher />
{@render children()}

<svelte:head>
  <link rel="stylesheet" href="/clinguin-theme.css" />
  <!-- TODO implement this so that it comes from the command line -->
  <link rel="stylesheet" href="/potassco-theme.css" />
</svelte:head>
