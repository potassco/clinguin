<script>
  /**
   * ErrorPage — full-screen split error display
   *
   * Props:
   *   code    {number|string}  — e.g. 404, 500, "403"
   *   title   {string}         — short label, e.g. "Page Not Found"
   *   message {string}         — detailed explanation shown on the right panel
   *
   * Usage in +error.svelte:
   *   import { page } from '$app/stores';
   *   <ErrorPage code={$page.status} title={$page.error?.name ?? 'Error'} message={$page.error?.message ?? ''} />
   */

  export let code = 404;
  export let title = "Page Not Found";
  export let message =
    "The page you are looking for does not exist or has been moved.";
</script>

<div class="error-page">
  <!-- Left panel — 70% blue -->
  <div class="panel-left">
    <div class="left-content">
      <div class="code-block">
        <span class="code-number">{code}</span>
        <span class="code-divider" aria-hidden="true"></span>
        <span class="code-title">{title}</span>
      </div>
    </div>
  </div>

  <!-- Right panel — 30% light -->
  <div class="panel-right">
    <div class="right-content">
      <p class="right-label">What happened</p>
      <p class="right-message">{message}</p>
    </div>
  </div>
</div>

<style>
  .error-page {
    display: flex;
    width: 100%;
    height: 100vh;
    min-height: 480px;
    font-family: var(--font-body);
  }

  .panel-left {
    flex: 0 0 70%;
    background-color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 4rem;
    position: relative;
    overflow: hidden;
  }

  .panel-right {
    flex: 0 0 30%;
    background-color: var(--secondary);
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 3rem 2.5rem;
    border-left: 1px solid var(--border);
  }

  .left-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
    position: relative;
    z-index: 1;
  }

  :global(.error-icon) {
    color: var(--muted-foreground);
  }

  .code-block {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
  }

  .code-number {
    font-size: clamp(4rem, 10vw, 7.5rem);
    font-weight: 700;
    color: var(--primary-foreground);
    letter-spacing: -0.03em;
    line-height: 1;
    font-family: var(--font-mono, monospace);
  }

  .code-divider {
    display: block;
    width: 2px;
    height: clamp(3rem, 7vw, 5.5rem);
    background-color: var(--muted-foreground);
    opacity: 0.3;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .code-title {
    font-size: clamp(1.25rem, 2.5vw, 2rem);
    font-weight: 400;
    color: var(--primary-foreground);
    opacity: 0.7;
    letter-spacing: -0.01em;
    line-height: 1.2;
    max-width: 16ch;
  }

  .right-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 28ch;
  }

  .right-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted-foreground);
    margin: 0;
  }

  .right-message {
    font-size: 0.975rem;
    line-height: 1.7;
    color: var(--secondary-foreground);
    margin: 0;
    white-space: pre-wrap;
  }

  @media (max-width: 640px) {
    .error-page {
      flex-direction: column;
      height: auto;
      min-height: 100vh;
    }

    .panel-left {
      flex: none;
      padding: 3rem 2rem;
    }

    .panel-right {
      flex: none;
      border-left: none;
      border-top: 1px solid var(--border);
      padding: 2.5rem 2rem;
    }

    .right-content {
      max-width: 100%;
    }

    .code-block {
      gap: 1rem;
    }
  }
</style>
