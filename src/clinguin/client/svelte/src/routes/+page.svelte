<script lang="ts">
  import { appContext } from "$lib/context.svelte";
  import Renderer from "$lib/Renderer.svelte";
  import { Toaster } from "$lib/components/ui/sonner";
  import Spinner from "$lib/components/internal/Spinner.svelte";
  import ErrorPage from "$lib/components/internal/ErrorPage.svelte";
</script>

{#await appContext.connectionPromise}
  {#if appContext.connected}
    <div class="fixed right-4 bottom-4">
      <Spinner />
    </div>
  {:else}
    <div class="fixed inset-0 flex items-center justify-center">
      <Spinner />
    </div>
  {/if}
{:catch err}
  <ErrorPage
    code={500}
    title="Connection Error"
    message={`Failed to connect to the server. \n\n${String(err.message ?? err)}`}
  />
{/await}

{#if appContext.error}
  <ErrorPage {...appContext.error} />
{:else if appContext.ui}
  <Renderer node={appContext.ui} />
{/if}

{#if appContext.loading}
  <div class="fixed right-4 bottom-4">
    <Spinner />
  </div>
{/if}

<Toaster />
