<script lang="ts">
  import { onMount } from 'svelte';
  import { appContext } from '$lib/context.svelte';
  import '../app.css';

  let { children } = $props();

  onMount(() => {
    appContext.connect();
  });
</script>

{@render children()}

<svelte:head>
  <link rel="stylesheet" href="/clinguin-theme.css">
</svelte:head>
