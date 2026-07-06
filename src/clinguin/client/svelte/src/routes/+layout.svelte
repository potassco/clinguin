<script lang="ts">
  import { onMount } from "svelte";
  import { appContext } from "$lib/context.svelte";
  import { ModeWatcher } from "mode-watcher";
  import "../app.css";

  let { children } = $props();

  const customTheme = import.meta.env.VITE_CUSTOM_THEME;

  onMount(() => {
    appContext.connect();
  });
</script>

<ModeWatcher />
{@render children()}

<svelte:head>
  <link rel="stylesheet" href="/clinguin-theme.css" />
  <!-- TODO implement this so that it comes from the command line -->
  {#if customTheme}
    <link rel="stylesheet" href={`/${customTheme}`} />
  {/if}
  <link rel="stylesheet" href={`${appContext.serverUrl}/static/generated.css`} />
</svelte:head>
