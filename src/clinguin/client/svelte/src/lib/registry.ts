import Text from '$lib/components/custom/Text.svelte';
import ThemeToggle from '$lib/components/custom/ThemeToggle.svelte';
import Icon from '$lib/components/custom/Icon.svelte';

export const registry: Record<string, any> = {
  text: Text,
  theme_toggle: ThemeToggle,
  icon: Icon,
};
