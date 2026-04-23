import Button from '$lib/components/Button.svelte';
import Container from '$lib/components/Container.svelte';
import Text from '$lib/components/Text.svelte';
//import Label from '$lib/components/Label.svelte';
import Sonner from '$lib/components/Sonner.svelte';

export const registry: Record<string, any> = {
  root: Container,
  window: Container,
  container: Container,
  text: Text,
  //label: Label,
  button: Button,
  sonner: Sonner,
  message: Sonner, // Temporary alias for backward compatibility with "message" attr in Sonner component
};
