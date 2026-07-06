# Svelte Frontend

Reference for the element types available in the SvelteKit frontend, and the attributes each one supports.

## Elements

### `container` / `window` / `root`

A generic box. `window`/`root` is the single top-level element; `container` is
used everywhere else for layout.

| Attribute | Values |
|---|---|
| `class` | Tailwind classes |
| `order` | numeric sort key among siblings |

```prolog
elem(w, window, root).
attr(w, class, ("min-h-screen"; "flex"; "flex-col"; "bg-muted")).

elem(header, container, w).
attr(header, class, ("flex"; "items-center"; "justify-between"; "px-6"; "py-4")).
attr(header, order, 1).
```

### `text`

| Attribute | Values |
|---|---|
| `text` / `label` | string content (either key works) |
| `class` | Tailwind classes |
| `order` | numeric sort key |

```prolog
elem(title, text, header_left).
attr(title, text, "Pigeonhole Assignment").
attr(title, class, ("text-xl"; "font-bold"; "text-primary")).
```

### `button`

| Attribute | Values |
|---|---|
| `text` / `label` | button label |
| `variant` | `default`, `secondary`, `destructive`, `outline`, `ghost`, `link` |
| `size` | e.g. `default`, `sm`, `xs` |
| `class`, `order` | as above |

```prolog
elem(next_btn, button, footer_right).
attr(next_btn, label, "Next solution").
attr(next_btn, variant, "outline").
attr(next_btn, order, 1).
when(next_btn, click, call, next_solution).
```

### `icon`

Used as a child of another element (button, text, dropdown item, ...).

| Attribute | Values |
|---|---|
| `icon` | [Lucide](https://lucide.dev/icons/) icon name in PascalCase (e.g. `"Bird"`, `"ArrowRight"`), or an image path/URL (`.svg`, `.png`, `.jpg`, `.jpeg`, `.webp`, or starting with `/`) |
| `icon_size` | Tailwind size class, e.g. `"size-4"` (default) |
| `order` | numeric sort key among siblings |

```prolog
elem(title_icon, icon, header_left).
attr(title_icon, icon, "Bird").
attr(title_icon, order, 1).
```

### `theme_toggle`

A light/dark mode toggle button.

| Attribute | Values |
|---|---|
| `icon_dark` | Lucide icon shown in dark mode (default `"Sun"`) |
| `icon_light` | Lucide icon shown in light mode (default `"Moon"`) |
| `variant`, `size` | same as `button` |
| `class`, `order` | as above |

```prolog
elem(toggle, theme_toggle, header_right).
attr(toggle, icon_dark, "Sun").
attr(toggle, icon_light, "Moon").
attr(toggle, variant, "outline").
```

### `sonner` (alias: `message`)

A one-time toast notification, shown when the element appears.

| Attribute | Values |
|---|---|
| `title` | toast title |
| `description` | optional body text |
| `type` | `success`, `warning`, `danger`, or `info` (default). **Note:** `error` is not a valid value — use `danger`. |

```prolog
elem(unsat_msg, sonner, w) :- _clinguin_unsat.
attr(unsat_msg, title, "Unsatisfiable!") :- _clinguin_unsat.
attr(unsat_msg, description, "No valid assignment exists with current constraints.") :- _clinguin_unsat.
attr(unsat_msg, type, danger) :- _clinguin_unsat.
```

### `dropdown_menu`

The trigger button that opens a menu. Needs a `dropdown_menu_content` child.
Nest a `dropdown_menu` inside another menu's content to get a submenu — no
separate submenu type is needed.

| Attribute | Values |
|---|---|
| `text` / `label` | trigger label |
| `class`, `order` | as above |

```prolog
elem(tools_menu, dropdown_menu, header_right).
attr(tools_menu, label, "Tools").
attr(tools_menu, class, ("border"; "rounded-md"; "px-3"; "py-2"; "text-sm")).
```

### `dropdown_menu_content`

The dropdown's panel. Child of a `dropdown_menu`.

| Attribute | Values |
|---|---|
| `align` | `start` (default), `center`, `end` |
| `side_offset` | number, default `4` |
| `class` | e.g. `"w-56"` to set a fixed width |

```prolog
elem(tools_content, dropdown_menu_content, tools_menu).
attr(tools_content, class, "w-56").
```

### `dropdown_menu_group`

Groups related items inside a menu and adds a separator above the group.

| Attribute | Values |
|---|---|
| `label` | optional heading for the group |
| `order` | numeric sort key among siblings |

```prolog
elem(danger_group, dropdown_menu_group, tools_content).
attr(danger_group, label, "Clear").
attr(danger_group, order, 2).
```

### `dropdown_menu_item`

A clickable row inside a menu (or a group).

| Attribute | Values |
|---|---|
| `text` / `label` | item label |
| `variant` | `default`, `destructive` |
| `inset` | `"true"`/`"false"` — indents to align with items that have icons |
| `checked` | if this attribute is set at all, the item becomes a checkbox item, checked when the value is `"true"` — omit entirely for a normal item |
| `order` | numeric sort key among siblings |

```prolog
elem(clear_item, dropdown_menu_item, danger_group).
attr(clear_item, label, "Clear assumptions").
attr(clear_item, variant, "destructive").
attr(clear_item, order, 1).
when(clear_item, click, call, clear_assumptions).
    elem(clear_icon, icon, clear_item).
    attr(clear_icon, icon, "Eraser").
```

### `dropdown_menu_label`

A non-interactive heading inside a menu (use this instead of a group's
`label` if the heading isn't tied to a specific group).

| Attribute | Values |
|---|---|
| `text` / `label` | heading text |
| `inset` | `"true"`/`"false"` |

### `dropdown_menu_radio_group`

Wraps a set of `dropdown_menu_radio_item` children for single-select.

| Attribute | Values |
|---|---|
| `value` | the currently selected value |

### `dropdown_menu_radio_item`

| Attribute | Values |
|---|---|
| `label` / `text` | item label |
| `value` | this item's value — matched against the parent group's `value` |

```prolog
elem(title_group_menu, dropdown_menu_radio_group, title_sub_content).
attr(title_group_menu, value, "Example").

elem(title_opt(P), dropdown_menu_radio_item, title_group_menu) :- title_option(P).
attr(title_opt(P), label, P) :- title_option(P).
attr(title_opt(P), value, P) :- title_option(P).
when(title_opt(P), click, update, (title_group_menu, value, P)) :- title_option(P).
```

## `when/4` actions

| Action | Effect |
|---|---|
| `call` | sends an operation to the backend, then refreshes the UI |
| `update` | updates one attribute in the UI directly, e.g. `(id, key, value)` |

```prolog
when(next_btn, click, call, next_solution).
when(title_opt(P), click, update, (title, text, P)) :- title_option(P).
```
