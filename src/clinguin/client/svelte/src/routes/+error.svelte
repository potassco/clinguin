<script>
	import { page } from "$app/stores";
	import ErrorPage from "$lib/components/internal/ErrorPage.svelte";
</script>

<ErrorPage
	code={$page.status}
	title={$page.error?.message ?? "Error"}
	message={$page.error?.message ?? "Something went wrong."}
/>
