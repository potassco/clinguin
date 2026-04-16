/**
 * Component registry — maps ASP element type names to Svelte components.
 *
 * Built-in types:
 *   root, window, container → Container (layout div)
 *   label                   → Label (display text)
 *   button                  → Button (shadcn Button)
 *   message                 → Message (toast notification via Sonner)
 *
 * TODO: make this extensible so users can register their own components with custom types.
 */

import Button from '$lib/components/Button.svelte';
import Container from '$lib/components/Container.svelte';
import Label from '$lib/components/Label.svelte';
import Message from '$lib/components/Message.svelte';

export const registry: Record<string, any> = {
  root: Container,
  window: Container,
  container: Container,
  label: Label,
  button: Button,
  message: Message
};
