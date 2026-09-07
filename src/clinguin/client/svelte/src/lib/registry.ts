import Button from '$lib/components/old/Button.svelte';
import Container from '$lib/components/custom/Container.svelte';
import Text from '$lib/components/custom/Text.svelte';
//import Label from '$lib/components/Label.svelte';
import Sonner from '$lib/components/custom/Sonner.svelte';
import ThemeToggle from '$lib/components/custom/ThemeToggle.svelte';
import Icon from '$lib/components/custom/Icon.svelte';
import DropdownMenu from '$lib/components/old/dropdown-menu/DropdownMenu.svelte';
import DropdownMenuContent from './components/old/dropdown-menu/DropdownMenuContent.svelte';
import DropdownMenuItem from './components/old/dropdown-menu/DropdownMenuItem.svelte';
import DropdownMenuGroup from './components/old/dropdown-menu/DropdownMenuGroup.svelte';
import DropdownMenuLabel from './components/old/dropdown-menu/DropdownMenuLabel.svelte';
import DropdownMenuRadioGroup from './components/old/dropdown-menu/DropdownMenuRadioGroup.svelte';
import DropdownMenuRadioItem from './components/old/dropdown-menu/DropdownMenuRadioItem.svelte';
import Checkbox from './components/old/Checkbox.svelte';
import Field from '$lib/components/old/field/Field.svelte';
import FieldSet from '$lib/components/old/field/FieldSet.svelte';
import FieldGroup from '$lib/components/old/field/FieldGroup.svelte';
import FieldLabel from '$lib/components/old/field/FieldLabel.svelte';
import FieldDescription from '$lib/components/old/field/FieldDescription.svelte';
import FieldError from '$lib/components/old/field/FieldError.svelte';
import Input from '$lib/components/old/Input.svelte';

export const registry: Record<string, any> = {
  root: Container,
  window: Container,
  container: Container,
  text: Text,
  //label: Label,
  //button: Button,
  sonner: Sonner,
  message: Sonner, // Temporary alias for backward compatibility with "message" attr in Sonner component
  theme_toggle: ThemeToggle,
  icon: Icon,
  /* dropdown_menu: DropdownMenu,
  dropdown_menu_content: DropdownMenuContent,
  dropdown_menu_item: DropdownMenuItem,
  dropdown_menu_group: DropdownMenuGroup,
  dropdown_menu_label: DropdownMenuLabel,
  dropdown_menu_radio_group: DropdownMenuRadioGroup,
  dropdown_menu_radio_item: DropdownMenuRadioItem, */
  //checkbox: Checkbox,
  //field: Field,
  //field_set: FieldSet,
  //field_group: FieldGroup,
  //field_label: FieldLabel,
  //field_description: FieldDescription,
  //field_error: FieldError,
  //input: Input

};
