<script lang="ts" module>
	import { type VariantProps, tv } from "tailwind-variants";

	export const alertVariants = tv({
		base: "grid gap-0.5 rounded-lg border px-4 py-3 text-left text-sm has-data-[slot=alert-action]:relative has-data-[slot=alert-action]:pr-18 has-[>svg]:grid-cols-[auto_1fr] has-[>svg]:gap-x-2.5 *:[svg]:row-span-2 *:[svg]:translate-y-0.5 *:[svg]:text-current *:[svg:not([class*='size-'])]:size-4 group/alert relative w-full",
		variants: {
			variant: {
				default: "bg-card text-card-foreground",
				destructive:
					"bg-card text-destructive *:data-[slot=alert-description]:text-destructive/90 *:[svg]:text-current",
			},
		},
		defaultVariants: {
			variant: "default",
		},
	});

	export type AlertVariant = VariantProps<typeof alertVariants>["variant"];
</script>

<script lang="ts">
	import XIcon from "@lucide/svelte/icons/x";
	import { cn, type WithElementRef } from "$lib/utils.js";
	import type { HTMLAttributes } from "svelte/elements";

	let {
		ref = $bindable(null),
		class: className,
		variant = "default",
		children,
		...restProps
	}: WithElementRef<HTMLAttributes<HTMLDivElement>> & {
		variant?: AlertVariant;
	} = $props();

	let dismissed = $state(false);
</script>

{#if !dismissed}
	<div
		bind:this={ref}
		data-slot="alert"
		role="alert"
		class={cn(alertVariants({ variant }), "pr-10", className)}
		{...restProps}
	>
		{@render children?.()}
		<button
			type="button"
			aria-label="Dismiss alert"
			class="absolute top-2 right-2 rounded p-1 opacity-0 transition-opacity focus-visible:outline-2 focus-visible:outline-ring group-hover/alert:opacity-100 group-focus-within/alert:opacity-100 [@mediaopacity-100"
			onclick={(event) => {
				event.stopPropagation();
				dismissed = true;
			}}
		>
			<XIcon class="size-4" />
		</button>
	</div>
{/if}
