<script lang="ts">
  import { appContext } from '$lib/context.svelte';
  import Renderer from '$lib/Renderer.svelte';
  import { Toaster } from '$lib/components/ui/sonner';
  import Loader2Icon from '@lucide/svelte/icons/loader-2';
</script>

{#await appContext.connectionPromise}
  <div class="clinguin-skeleton" style="width: 100%; height: 120px;"></div>
{:then}
  {#if appContext.ui}
    <Renderer node={appContext.ui} />
  {:else}
    <p class="clinguin-status">No UI loaded.</p>
  {/if}
{:catch err}
  <pre class="clinguin-error">{err.message}</pre>
{/await}

{#if appContext.loading}
  <div class="clinguin-loading">
    <Loader2Icon class="size-4 animate-spin" />
  </div>
{/if}

{#if appContext.error}
  <pre class="clinguin-error">{appContext.error}</pre>
{/if}

<Toaster />
