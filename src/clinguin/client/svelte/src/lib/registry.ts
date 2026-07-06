import Button from '$lib/components/Button.svelte';
import Container from '$lib/components/Container.svelte';
import Text from '$lib/components/Text.svelte';
//import Label from '$lib/components/Label.svelte';
import Sonner from '$lib/components/Sonner.svelte';
import ThemeToggle from '$lib/components/ThemeToggle.svelte';
import Icon from '$lib/components/Icon.svelte';
import DropdownMenu from '$lib/components/dropdown-menu/DropdownMenu.svelte';
import DropdownMenuContent from './components/dropdown-menu/DropdownMenuContent.svelte';
import DropdownMenuItem from './components/dropdown-menu/DropdownMenuItem.svelte';
import DropdownMenuGroup from './components/dropdown-menu/DropdownMenuGroup.svelte';
import DropdownMenuLabel from './components/dropdown-menu/DropdownMenuLabel.svelte';
import DropdownMenuRadioGroup from './components/dropdown-menu/DropdownMenuRadioGroup.svelte';
import DropdownMenuRadioItem from './components/dropdown-menu/DropdownMenuRadioItem.svelte';

export const registry: Record<string, any> = {
  root: Container,
  window: Container,
  container: Container,
  text: Text,
  //label: Label,
  button: Button,
  sonner: Sonner,
  message: Sonner, // Temporary alias for backward compatibility with "message" attr in Sonner component
  theme_toggle: ThemeToggle,
  icon: Icon,
  dropdown_menu: DropdownMenu,
  dropdown_menu_content: DropdownMenuContent,
  dropdown_menu_item: DropdownMenuItem,
  dropdown_menu_group: DropdownMenuGroup,
  dropdown_menu_label: DropdownMenuLabel,
  dropdown_menu_radio_group: DropdownMenuRadioGroup,
  dropdown_menu_radio_item: DropdownMenuRadioItem,

};
