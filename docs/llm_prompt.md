# Self-contained prompt for generating a Clinguin v3 UI

Copy the two blocks separately and send them to the LLM in this order:

1. Copy **Part I** unchanged. It is the fixed Clinguin v3 reference.
2. Fill in **Part II**, then copy it as the application-specific input.

Each code block has its own copy button in the upper-right corner.

## Copy Part I — Immutable Clinguin v3 reference

~~~~text
## Part I — Immutable Clinguin v3 reference

### 1. Role and ground rules

You are an expert in Answer Set Programming (ASP), clingo, and Clinguin v3.
Generate runnable Clinguin v3 UI code from Part II.

- The UI is an ASP encoding: `.lp` files that derive Clinguin predicates. Never
  replace it with Svelte, JavaScript, TypeScript, or static HTML. Clinguin's
  frontend renders it with native HTML elements, installed shadcn-svelte
  components, and Clinguin components.
- Use only the components, attributes, events, operations, and conventions
  defined in this prompt. Never invent an API.
- Links in Part II are provenance only; assume you cannot open them. Everything
  you need is in this prompt and the files pasted into Part II.
- Treat any unfilled `[...]` placeholder in Part II as missing information.
- If missing information affects correctness and no safe default exists, ask
  one short question. Otherwise make the smallest reasonable assumption and
  list it in the result.
- Part II §4 (Permissions) decides which optional mechanisms you may use. An
  unticked permission means "not allowed".
- A custom backend operation may be used only when Part II supplies its exact
  operation term, behavior, state effects, backend/run configuration, and
  explicitly permits calling it. Otherwise treat it as unavailable.
- If a principal workflow cannot be implemented with the supplied files and
  supported APIs, the result is **BLOCKED** (Section 8.2).

### 2. Runtime and application structure

#### 2.1 How Clinguin works

```text
domain files → domain control ← backend operations
                       ↓
              domain state + UI files
                       ↓
                 fresh UI control
                       ↓
             elem/3 + attr/3 + when/4
                       ↓
                  Svelte frontend
```

- **Domain control:** long-lived clingo control holding the problem and
  instance. It survives UI refreshes. Backend operations change its
  assumptions, browsed solution, externals, dynamic atoms, constants, grounded
  programs, or active files.
- **Domain state:** facts describing the current solver and interaction state
  (Section 4).
- **UI control:** created fresh on every refresh from the UI files plus the
  current domain state. Only `elem/3`, `attr/3`, and `when/4` are sent to the
  frontend.

The UI is declarative. Values, selection, disabled state, and available
actions must be re-derived from domain state after every backend call, never
kept as hidden browser state. The domain control is the source of truth.

#### 2.2 Quick-start project

Unless Part II supplies another v3 structure to preserve, assume the project
was created with:

```console
clinguin init my-ui
```

which produces `ui.lp` and `menu-bar.lp`. `ui.lp` already contains this
framework-owned scaffold, followed by the application marker comment
(exact comment wording may differ):

```prolog
#include "menu-bar.lp".

elem(ui_app, div, root).
attr(ui_app, class,
    ("min-h-screen"; "flex"; "flex-col";
     "bg-background"; "text-foreground")).

elem(ui_content, main, ui_app).
attr(ui_content, class,
    ("flex"; "min-h-0"; "grow"; "flex-col")).
attr(ui_content, order, 100).

% APPLICATION UI
```

Rules for the scaffold:

- `root` is supplied by Clinguin; never define it.
- Never repeat, rename, restyle, or redefine the include, `ui_app`,
  `ui_content`, or their attributes. Write all application rules below the
  `APPLICATION UI` marker.
- Attach page content to `ui_content`. For width, padding, or grid layout,
  create and style a child (e.g. `app_page`) instead of changing `ui_content`.
- Configure the menu bar from the application section, not by editing
  `menu-bar.lp`:

  ```prolog
  menubar_title_override("My Application").
  menubar_subtitle_override("What this application does").
  menubar_icon_override("Menu").
  ```

  Put global status under `menubar_center` and application-level actions
  under `menubar_right`.
- A v2 `ui.lp` supplied for migration is source material, not the scaffold.
- Larger UIs may use additional included `.lp` files. Keep solving logic in
  domain files and presentation logic in UI files.

Typical run command when both example domain files exist:

```console
clinguin share --domain-files encoding.lp instance.lp --ui-files ui.lp
```

The final command must instead use the exact supplied/generated file list and
preserve any required backend or CLI options from Part II. Omit absent files;
never name `instance.lp`, `menu-bar.lp`, or another file that was not supplied
or generated.

### 3. Core UI predicates

#### 3.1 Elements: `elem(ID, Type, Parent)`

- `ID`: unique, stable identifier. Lowercase constants for fixed elements,
  function terms for repeated ones; never build IDs from display text.
- `Type`: a supported type (Section 6). Compound component members use
  `family(member)`.
- `Parent`: an existing element ID, or `root`.

```prolog
elem(page, section, ui_content).
elem(item(Name), div, page) :- item_data(Name).

elem(help, dialog, page).
elem(help_trigger, dialog(trigger), help).
elem(help_content, dialog(content), help).
```

Every ID has exactly one type and one parent; the parent relation is acyclic.

#### 3.2 Attributes: `attr(ID, Key, Value)`

```prolog
attr(page_title, text, "Available courses").
attr(save_button, variant, "default").
attr(save_button, disabled, true) :- not form_valid.
attr(panel, class, ("rounded-lg"; "border"; "p-4")).
```

- Strings for displayed text, numbers for numeric properties, `true`/`false`
  for Booleans. Use the exact key documented for the component.
- Multiple values for one key are joined with spaces (useful for `class`).
  Scalar keys (`text`, `value`, `disabled`, `variant`, `size`, …) must have at
  most one value in any UI state.
- General keys: `text` (or `content`) for rendered text, `class` for Tailwind
  classes, `order` for numeric sibling order (default `0`; give siblings
  distinct values when order matters).

#### 3.3 Interactions: `when(ID, Event, Action, Operation)`

| Field | Meaning |
| --- | --- |
| `ID` | Element receiving the event. |
| `Event` | Event name without `on` prefix (Section 5.2). |
| `Action` | `update`, `context`, or `call` (Section 5.2). |
| `Operation` | Data for that action. |

```prolog
when(details_button, click, update, (details_panel, hidden, false)).
when(name_input, input, context, (person_name, _value)).
when(clear_button, click, call, clear_assumptions).
```

Never infer an operation from a control's visible text.

#### 3.4 Conditional and repeated UI

```prolog
elem(person_row(P), div, people_list) :- person(P).
attr(person_row(P), class, "bg-primary/10") :- selected(P).

elem(empty_message, p, people_list) :- not person(_).
attr(empty_message, text, "No people available") :- not person(_).

when(person_row(P), click, call, add_assumption(selected(P), true)) :-
    selectable(P).
```

Derive an attribute or action only when its element exists. Use small helper
predicates when several rules share a condition.

#### 3.5 ASP correctness

- End every fact, rule, directive, and include with a period.
- Make every variable safe (positive body literals, finite ranges, safe
  arithmetic).
- Quote user-facing strings; escape contained `"` and `\`.
- Every non-domain, non-reserved predicate used in a rule body must be defined
  in the generated UI (e.g. `selected/1`, `has_items/0`).
- Derive one deterministic UI per domain state; no choice rules for layout.
- Do not redefine `elem/3`, `attr/3`, or `when/4`.
- No v2-only types such as `window` or `container`.

#### 3.6 UI string helpers

The UI control is grounded with these functions. Use them when displayed text
must be constructed dynamically; do not invent other `@` functions.

| Function | Result |
| --- | --- |
| `@concat(A, B, ...)` | Concatenate the textual form of all arguments. |
| `@format(Template, A, B, ...)` | Fill Python-style `{}` / `{0}` fields in `Template`. |
| `@format(Template, (A, B, ...))` | Tuple form of the same formatting operation. |
| `@stringify(Value)` | Replace underscores with spaces. |
| `@stringify(Value, true)` | Also capitalize the first character. |
| `@upper(Value)` | Convert text to uppercase. |

```prolog
attr(day_heading(D), text, @format("{} {}", (Weekday, D))) :-
    day(D, Weekday).
attr(item_name(I), text, @stringify(I, true)) :- item(I).
```

### 4. Domain-state predicates

The backend adds these as facts to every UI control. Predicates beginning with
`_clinguin_`, plus `_any/1`, `_all/1`, `_any_opt/1`, `_all_opt/1`, are
reserved: read them, never define them. All reflect the current assumptions,
externals, dynamic atoms, constants, active files, and grounding.

#### 4.1 Models and consequences

Current-model atoms appear directly, e.g. `assigned(anna, room_1).` They come
from one backend-selected model (the browsed model while browsing), not
necessarily from every model. If the domain becomes unsatisfiable, stale model
atoms may remain, so guard model-dependent UI with `not _clinguin_unsat` and
always render an explicit unsatisfiable state.

| Predicate | `A` occurs in … |
| --- | --- |
| `_any(A)` | at least one stable model |
| `_all(A)` | every stable model |
| `_any_opt(A)` | at least one optimal stable model |
| `_all_opt(A)` | every optimal stable model |

```prolog
available(P, R) :- _any(assigned(P, R)).
certain(P, R)   :- _all(assigned(P, R)).
```

Consequence computation is expensive; use it for solver guidance, not as a
default replacement for current-model atoms.

#### 4.2 Solver and interaction state

| Predicate | Meaning |
| --- | --- |
| `_clinguin_unsat` | Current domain state is unsatisfiable. |
| `_clinguin_browsing` | Backend is browsing models (`next_solution`). |
| `_clinguin_assume(A, true/false)` | User explicitly assumed `A` true/false. |
| `_clinguin_optimizing` | Current model has an optimization cost. |
| `_clinguin_optimal` | Optimality proven for the current model. |
| `_clinguin_cost(Tuple)` | Full cost tuple; `_clinguin_cost(())` when no cost. |
| `_clinguin_cost(Index, Value)` | Zero-based cost component. |
| `_clinguin_context(Key, Value)` | Context submitted with the latest call. |
| `_clinguin_const(Name, Value)` | Active domain constant. |
| `_clinguin_atom(A)` | Atom added dynamically through the backend. |
| `_clinguin_external(A, true/false/release)` | External assignment. |
| `_clinguin_message(ID, Type, Title, Content)` | Backend message; `Type` is normally `info`, `success`, `warning`, or `error`. |

- An assumption is an explicit user decision; `_all(A)` is a solver
  consequence. Keep that distinction visible when explaining a value.
- Test `_clinguin_optimizing`, not the existence of `_clinguin_cost/1`.
- Context is temporary, not durable storage. The browser clears its pending
  context after a successful call, but the backend's `_clinguin_context/2`
  facts describe the most recently submitted call until a later operation
  replaces them. `_clinguin_atom/1` and externals describe backend
  manipulation; the same atom may also appear in the model.
- Render relevant `_clinguin_message/4` facts as persistent page alerts when
  users must retain the information. A transient `sonner` alone is insufficient.

#### 4.3 Optional uploaded files

Only when Part II requests file behavior:

| Predicate | Meaning |
| --- | --- |
| `_clinguin_optional_file(Name)` | Uploaded file available. |
| `_clinguin_active_file(Name)` | Uploaded file active in the domain. |
| `_clinguin_file_content(Name, Content)` | Uploaded text content. |

Treat names and contents as untrusted; do not display full contents by default.

#### 4.4 Domain–UI contract

- Assumed atoms must exist in the grounded domain.
- UI-controlled externals must be declared with `#external`.
- The contract is the named domain predicates, not `#show`. Never emit an
  unnamed tuple such as `#show (X,Y) : p(X,Y).`

### 5. Events, actions, and backend operations

#### 5.1 Choose the state mechanism

| Intent | Mechanism |
| --- | --- |
| Restrict the solution space temporarily | Assumptions |
| Inspect complete solutions | Model browsing |
| Add/remove session data (needs permission) | Dynamic atoms |
| Control declared multi-shot switches | Externals |
| Submit temporary input | Context |
| Change presentation until next refresh | Local `update` |

Prefer assumptions over dynamic atoms for temporary restrictions. Never use
context or local updates as solver state.

#### 5.2 Events, actions, and the two central rules

Native events: `click`, `input`, `change`, form `submit`. Component callbacks
map to `open_change`, `value_change`, `checked_change` (Section 6.4).

| Action | Operation | Effect |
| --- | --- | --- |
| `update` | `(TargetID, Key, Value)` | Change one rendered attribute until refresh. |
| `context` | `(Key, Value)` | Store data for the next call. |
| `call` | One backend operation term | Submit current context, run it, clear the browser's pending context on success, and recompute UI. |

For one element and event, `update` and `context` actions run before `call`;
order within each group is unspecified. Keep `update` values free of
unprotected commas (the operation is parsed textually).

**Rule A — one call.** In any UI state, each element/event pair has at most
one `call`. v2 tuples of ordered calls are not supported; every call is a
separate request and refresh.

**Rule B — user-level actions only.** A control expresses one user goal.
Never turn grounding, external assignment, cache updates, browsing setup, or
other solver lifecycle steps into extra buttons or required user steps. Split
a workflow only when every step is independently meaningful to the user. If
one user goal needs several ordered backend operations, it requires a tested
application-level backend operation or an atomic batch capability: report
that, and do not simulate it. (This is the most common cause of BLOCKED.)

#### 5.3 Context, forms, and substitution

```prolog
when(pet_item(P), click, context, (selected_pet, P)) :- pet(P).
when(name_input, input, context, (person_name, _value)).
```

- `_value` is the event value: an ASP string for text inputs, a number for
  number/range inputs; component values must be valid ASP terms.
- Context is sent with the next call and appears as `_clinguin_context/2` in
  the resulting UI state. The browser's pending context is then cleared, while
  the backend retains those facts until the next operation replaces them.
- On form `submit`, native submission is prevented and every named control is
  added to context automatically; no per-input context actions are needed:

```prolog
elem(person_form, form, ui_content).
when(person_form, submit, call,
    add_atom(person(_context_value(name, "Anonymous"),
                    _context_value(age, 0)))).

elem(name_input, input, person_form).
attr(name_input, name, "name").
elem(age_input, input, person_form).
attr(age_input, name, "age").
attr(age_input, type, "number").

elem(add_button, button, person_form).
attr(add_button, type, "submit").
attr(add_button, text, "Add person").
```

- Substitute context inside a call with `_context_value(Key)` (rejects
  missing or empty input) or `_context_value(Key, Default)`. Substitution is
  recursive; the result must parse as an ASP term. v2 forms with a type
  argument are unsupported: in v3 a second argument is always a default.
- A file input contributes its file name to context and its content
  separately; for an input named `instance`, use
  `activate_file(_context_value(instance))`.

#### 5.4 Backend operation catalogue

A `call` names one public backend method listed here, or a custom operation
explicitly documented and permitted in Part II. Never call private methods,
`get`, or arbitrary Python methods. Rule B applies to all of them.

**Assumptions**

| Operation | Effect |
| --- | --- |
| `add_assumption(A)` / `add_assumption(A, Bool)` | Assume `A` true / `Bool`. |
| `remove_assumption(A)` | Remove the recorded assumption for exactly `A`. |
| `remove_assumption_signature(Pattern)` | Remove matches; `any` is a positional wildcard. |
| `clear_assumptions` | Remove all assumptions. |

Adding does not replace an existing assumption on the same atom: remove the
old value before offering its opposite.

**Browsing**

| Operation | Effect |
| --- | --- |
| `next_solution` / `next_solution(ignore)` | Start or advance browsing. |
| `next_solution(optN)` | Start or advance optimal-model browsing. |
| `stop_browsing` | End browsing without selecting. |
| `select` | Assume the browsed model, stop browsing. Only while `_clinguin_browsing`. |
| `select(ShowProgram)` | Same, keeping only atoms retained by the show program. |

```prolog
when(select_button, click, call, select("#show assigned/2.")) :-
    _clinguin_browsing.
```

**Dynamic atoms, externals, files**

| Operation | Effect |
| --- | --- |
| `add_atom(A)` / `remove_atom(A)` / `clear_atoms` | Add/remove dynamic facts, then rebuild and ground. Needs permission. |
| `set_external(A, true/false)` | Assign a declared external. |
| `set_external(A, release)` | Permanently release it (not the same as false). |
| `activate_file(Name)` / `deactivate_file(Name)` | Only for files received through a Clinguin file input. |

**Lifecycle, grounding, constants**

| Operation | Effect |
| --- | --- |
| `update` | Clear cached domain-state computations and recompute. |
| `restart` | Restore CLI configuration; clears assumptions, atoms, externals, files, browsing, context. |
| `set_constant(Name, Value)` | Change a constant and reinitialize interactive state. |
| `ground(Program)` | Ground a zero-argument `#program` part. Technical interface only (needs permission). |

Expose `restart` and `set_constant` only when the reset scope is clear to the
user. `ground(Program, Argument)` is not supported in generated UIs; a
workflow that needs parameterized grounding, or grounding combined with other
ordered operations, falls under Rule B.

**Server-side export** (needs permission)

| Operation | Effect |
| --- | --- |
| `download` | Write the current model to a file on the Clinguin server. |
| `download(ShowProgram, FileName)` | Write a filtered model to a server file. |

This is not a browser download. It needs a current model and must run before
`select`.

**Name collisions:** the backend `update` operation and `select` operation are
unrelated to the local `update` action and the `select` component. The `text`
attribute is unrelated to the `text` component.

#### 5.5 Errors and concurrency

Invalid operations, missing context, parse errors, and rejected files are
reported by the frontend. Backend operations are not generally transactional:
an operation that fails after mutating backend state may require recovery with
a corrective operation or `restart`. Do not promise rollback unless the
supplied custom operation is explicitly documented and tested as atomic. Each
call carries the UI version: if another client changed the backend, the stale
call is rejected and the UI refreshes. Always derive controls and labels from
refreshed state.

### 6. Frontend components and styling

#### 6.1 Type resolution

A type resolves to, in order: a registered Clinguin component, an installed
shadcn-svelte family, a valid HTML tag, otherwise an error. Use semantic HTML
for ordinary structure (landmarks, headings, paragraphs, lists, tables,
links, images). Types shared with HTML (`button`, `input`, `label`, `select`,
`textarea`) resolve to the styled component.

#### 6.2 Root components

| Type | Main attributes / events |
| --- | --- |
| Native HTML | `text` plus standard HTML attributes, spelled exactly |
| `button` | `text`, `variant`, `size`, `type`, `disabled`, `href`; `click` |
| `input` | `type`, `name`, `value`, `placeholder`, constraints; `input`, `change` |
| `textarea` | `name`, `value`, `placeholder`, `rows`; `input`, `change` |
| `checkbox` | `checked`, `indeterminate`, `name`, `value`; `checked_change` |
| `label` | `text`, `for` |
| `select` | `type` (use `"single"`), `value`, `name`; `value_change` |
| `separator` | `orientation`, `decorative` |
| `alert` | `variant`: `default` / `destructive` |
| `skeleton`, `spinner` | size via `class` |
| `dialog`, `sheet`, `dropdown_menu` | `open`; `open_change` |
| `tabs` | `value`; `value_change` |
| `field` | `orientation` |
| `sidebar` | provider/root/content/menu members |
| `text` | `text`; prefer semantic HTML in new code |
| `icon` | `icon` (exact Lucide PascalCase name or image path), `icon_size`, `class` |
| `theme_toggle` | `variant`, `size`, optional `icon_light`, `icon_dark` |
| `sonner` | `title`, `description`, `type`: `info`/`success`/`warning`/`danger` |

Button variants: `default`, `outline`, `secondary`, `ghost`, `destructive`,
`link`. Sizes: `default`, `xs`, `sm`, `lg`, `icon`, `icon-xs`, `icon-sm`,
`icon-lg`.

#### 6.3 Compound members

Every member is typed with its family, e.g. `title` under `dialog` means
`dialog(title)`.

```text
alert          > title + description + [action]
dialog, sheet  > trigger + content(header(title + description)
                                   + native-body + [footer(close)])
dropdown_menu  > trigger + content([label] + items
                                   + [groups/separators/checkbox/radio/submenu])
select         > trigger + content([label] + items + [groups/separators])
tabs           > list(one trigger per value) + one content per value
tooltip        > provider(tooltip(trigger + content))
field(set)     > legend + group(field(label + control + [description] + [error]))
sidebar        > provider(sidebar(header + content(groups/menus) + footer)
                          + [inset])
```

`native-body` above means an ordinary semantic HTML element such as `div`,
`section`, or `form`; there is no `dialog(body)` or `sheet(body)` member.

| Member | Key attributes / events |
| --- | --- |
| any `trigger`, `close` | `text`, `class` (already a button primitive) |
| `title`, `description`, `label`, `legend` | `text` |
| `select(item)` | `value` (valid ASP term), `label`, `disabled` |
| `tabs(trigger)`, `tabs(content)` | `value` (identical for a matching pair) |
| `dropdown_menu(item)` | `text`, `disabled`; `click` |
| `dropdown_menu(checkbox_item)` | `checked`; `checked_change` |
| `dropdown_menu(radio_group)` / `(radio_item)` | `value`; group `value_change` |
| `field(label)` | `text`, `for` |
| `field(description)`, `field(error)` | `text` |

Example:

```prolog
elem(help, dialog, actions).
elem(help_trigger, dialog(trigger), help).
attr(help_trigger, text, "Help").
attr(help_trigger, class,
    ("inline-flex"; "h-9"; "items-center"; "rounded-md"; "border"; "px-3")).
elem(help_content, dialog(content), help).
elem(help_header, dialog(header), help_content).
elem(help_title, dialog(title), help_header).
attr(help_title, text, "How to use this application").
elem(help_description, dialog(description), help_header).
attr(help_description, text, "Choose valid values, then confirm the result.").
```

Use simpler semantic HTML when it conveys the same structure; do not add a
sidebar just to arrange a small page.

#### 6.4 Component rules

- Children render before an element's own `text`.
- Other properties are forwarded with their exact Svelte spelling, including
  camelCase (`sideOffset`, `showCloseButton`, `closeOnSelect`, `textValue`,
  `preventScroll`). If an unlisted property cannot be verified, use a listed
  or native HTML alternative.
- Callbacks: `onOpenChange` → `open_change`, `onValueChange` →
  `value_change`, `onCheckedChange` → `checked_change`. The callback value is
  `_value`; capture it with a `context` action before a `call` when needed.
- Never nest a `button` inside a trigger or close member; style it with
  `class`.
- Do not add portals or positioning internals for dialog, dropdown, select,
  sheet, or tooltip; the wrappers create them.
- Derive `select` trigger text explicitly from current state.
- Generate `field(error)` conditionally with an explicit error class.
- `theme_toggle` already has its icon, label, and click behavior; add no
  children or actions.
- Sonner toasts are transient; persistent states must also appear on the page.

#### 6.5 Tailwind and theme

- Style only through `class`. Clinguin generates CSS by scanning UI files at
  startup, so every class must appear as a complete literal; never assemble
  class names from fragments.
- Write modifiers literally: `"md:flex-row"`, `"hover:bg-muted"`. Never write
  `"md\:flex-row"`: `\:` is an invalid clingo escape and a lexer error.
- Prefer semantic theme classes (`bg-background`, `text-foreground`,
  `bg-card`, `bg-muted`, `text-muted-foreground`, `bg-primary`,
  `text-primary-foreground`, `border-border`, `border-input`,
  `text-destructive`). Use fixed colors or `dark:` only when no semantic class
  fits. No custom CSS unless Part II asks for it.
- Mobile first; add `sm:`/`md:`/`lg:`/`xl:` changes. Flex for one-dimensional
  groups, grid for repeated rows/columns. Add `min-w-0` to flexible children,
  let action groups wrap, wrap wide tables in `overflow-x-auto`. No absolute
  positioning; never hide essential content.
- Base classes unconditional, state classes conditional:

```prolog
attr(card(P), class, ("rounded-lg"; "border"; "bg-card"; "p-4")) :- person(P).
attr(card(P), class, ("border-primary"; "ring-2")) :- selected(P).
```

#### 6.6 Accessibility

- Semantic landmarks, headings, lists, and tables (with captions and header
  cells).
- Buttons for actions, links for navigation.
- Every form control has a visible associated label; a tooltip never replaces
  it.
- Dialog and sheet content has a title (and normally a description).
- Icons are decorative: put interactive icons inside a labeled control; give
  icon-only controls `sr-only` text. Never invent icon names.
- Informative images get alt text; decorative images get empty alt.
- Never convey validity, selection, or solver status by color alone; pair it
  with text or a control property.
- Show errors next to affected controls; show application-wide errors
  persistently.
- Use real `disabled`, `required`, checked, and selected properties. Prefer
  built-in semantics over ARIA.

### 7. Migrating from Clinguin v2

Treat a v2 UI as a behavioral specification: preserve its domain behavior and
principal workflow, rebuild its structure with the rules above. Keep stable
IDs where they don't obscure the new hierarchy. Do not change the domain to
imitate a removed widget unless Part II permits it.

| v2 | v3 |
| --- | --- |
| `elem(w, window, root)` | Use `ui_app`; attach content to `ui_content`. |
| `container` | `div`, `main`, `section`, `nav`, … |
| `text` for headings/labels | `span`, `p`, heading elements |
| `attr(ID, label, T)` | `attr(ID, text, T)` |
| Bootstrap classes | Complete Tailwind classes |
| `"true"` / `"false"` strings | `true` / `false` |
| `message`, type `error` | `sonner`, type `danger` |
| `dropdown_menu_content`, `_item`, `_radio_group` | `dropdown_menu(content)`, `(item)`, `(radio_group)` |
| `field_set`, `_group`, `_label`, `_description`, `_error` | `field(set)`, `(group)`, `(label)`, `(description)`, `(error)` |
| Labeled dropdown | `dropdown_menu > trigger + content`; label → trigger `text` |
| Flat dialog/sheet/select/tabs | Full member structure from Section 6.3 |
| Field `invalid` attribute | Conditional `field(error)` with explicit class |
| Several calls / ordered call tuple per event | Rule A and Rule B (Section 5.2) |
| `_context_value(Key, Type)` | `_context_value(Key)` |
| `_context_value(Key, Type, Default)` | `_context_value(Key, Default)` |
| Window `load` restoring context | Persist state in the backend; derive after refresh |
| Old component events | v3 callback events (Section 6.4) |
| Operation not in Section 5.4 | Redesign the workflow or report the needed capability |
| `draggable_as`, implicit drag/drop, unlisted custom elements | Replace with supported controls or report as not migratable |

Recheck every operation and context substitution against Sections 4–5. Prefer
named form controls with form submission over many input handlers.

### 8. Generation procedure

#### 8.1 Understand

Read Part II. Note the mode (`migrate_v2` or `create_new`), permissions,
domain predicates, required workflows, edge states, and requested files. For
a migration, inventory the v2 regions, conditional UI, events, context keys,
operations, and visible behavior, and classify each as reusable, direct
mapping, structural rewrite, or unsupported.

#### 8.2 Plan and apply the capability gate

1. Describe each interaction as a user goal, then pick its mechanism
   (Section 5.1) and check Rules A and B.
2. **Capability gate:** every principal user action, including any
   initialization it depends on, must have a complete supported state
   transition from the initial runtime state, using only permitted mechanisms.
3. If any principal action fails the gate, the result is **BLOCKED**: write
   no application code. A permanently disabled control, a limitation notice,
   or a display-only page is not an implementation. Report the first
   unavailable transition, the exact operation or permission it needs, and the
   smallest change that would unblock it.
4. Otherwise, plan the element hierarchy and the normal, empty, browsing,
   unsatisfiable, validation, and recovery states. Semantic HTML first;
   registered components only where their behavior helps.

#### 8.3 Generate

Generate the smallest interface that satisfies Part II, using Sections 2–6.
Add no help dialogs, tutorials, legends, decorative sections, duplicate
status displays, or extra actions unless requested or needed for a required
workflow. Keep any permitted domain changes separate from UI files. Create an
extra included UI file only when needed.

### 9. Output format

Unless Part II requests otherwise, return in this order.

#### 9.1 Summary

- Application structure and primary workflow.
- Assumptions made.
- Unsupported requirements or needed custom capabilities (never hidden in
  code comments).

#### 9.2 Migration mapping (`migrate_v2` only)

| v2 behavior or structure | v3 implementation | Status |
| --- | --- | --- |

Cover every principal interaction and every changed or unpreserved behavior.

#### 9.3 Files

Depending on the output choice in Part II §5:

- **Application section (default):** one fenced `prolog` block labeled
  `ui.lp — APPLICATION UI section`, containing only the rules below the
  marker; no scaffold, include, or `menu-bar.lp`.
- **Complete `ui.lp`:** when the quick-start scaffold exists, preserve it
  unchanged and append the application rules; otherwise generate the complete
  scaffold required by the result.
- **All changed or new files:** a file tree, then each file in its own fenced
  block labeled with its path.

If Part II says the quick-start files do not exist, an application section is
not a runnable result: return at least a complete `ui.lp`. Include
`menu-bar.lp` only when it is explicitly confirmed to exist or its complete
contents are supplied or generated; never emit an include for a missing file.
If Part II supplies an existing customized v3 `ui.lp`, preserve its scaffold
and return the requested complete changed file when an application-only
section would be ambiguous.

No ellipses, pseudocode, "existing code here", or missing helper definitions.
Explain why each permitted domain change is needed. For **BLOCKED**, return no
code blocks and no run command (unless Part II explicitly asks for a partial
artifact).

#### 9.4 Run command and verification

Give the exact run command (runnable results only). Then perform and report
each check below using only: **PASS** (executed, succeeded), **FAIL**
(executed, failed), **NOT RUN** (environment did not allow it), **BLOCKED**
(information or capability missing). Never mark a check PASS because the code
looks correct. For every non-PASS item, give the reason and the next concrete
verification step.

| Check | What to verify |
| --- | --- |
| ASP parsing/grounding | All domain and UI files parse and ground; no `\:` or other invalid escapes. |
| UI structure | Unique IDs, valid parents, compound hierarchies, aligned conditions, all helper predicates defined. |
| API conformance | Every type, attribute, event, context substitution, and operation exists in this prompt; no v2 syntax. |
| Rules A and B | At most one call per element/event in any state; no exposed lifecycle choreography. |
| Initial render | Normal or empty initial state renders without frontend errors. |
| Interactions | Each event performs its intended single operation. |
| State refresh | UI reflects backend state after calls; nothing depends on stale local state. |
| Edge states | Unsatisfiable, empty, validation, and browsing states work as required. |
| Responsive/accessibility | Literal Tailwind classes, layout, labels, focus, persistent errors. |
| Migration parity | (`migrate_v2`) principal v2 workflows behave equivalently. |

#### 9.5 Final self-check

Confirm: no invented API, no v2 syntax, no missing file or include, no
unpermitted domain change, all assumptions and unverified behavior listed.

~~~~

## Copy Part II — User input template

Fill in every required placeholder inside this block before copying it.

~~~~text
## Part II — User input

Replace every `[...]`. Fields marked *(optional)* may be deleted.

### 1. Task

**Mode** (keep one): `create_new` | `migrate_v2`

**What should the application do?**
[One or two sentences. Example: "Lets a planner assign people to rooms and
see which assignments are still possible."]

**Who will use it?** *(optional)*
[e.g. "students", "administrators", "general users"]

### 2. Files

Paste every relevant file. Copy a block for each additional file (extra
instances, included UI files, a custom `menu-bar.lp`).

--- BEGIN FILE: encoding.lp ---
[paste file]
--- END FILE: encoding.lp ---

--- BEGIN FILE: instance.lp ---
[paste file or write "none"]
--- END FILE: instance.lp ---

--- BEGIN FILE: ui.lp ---
[for migrate_v2: paste the old UI; for create_new: paste any existing v3 UI,
or write "none"]
--- END FILE: ui.lp ---

**How do you currently run it?**
[e.g. `clinguin share --domain-files encoding.lp instance.lp --ui-files ui.lp`,
or "not yet"]

### 3. Required behavior

**What should users be able to do?** (one action per line, in user terms)

- [Example: "Click a person, then a room, to fix that assignment."]
- [Example: "Undo one fixed assignment, or reset all."]
- [action]

**What should the UI show?**

- [Example: "A grid of rooms with the people assigned in the current solution."]
- [Example: "Which assignments are certain and which are only possible."]
- [information]

**Migration only — behavior that must be preserved:**
[list, or "preserve the current workflow"]

### 4. Permissions

Tick with `[x]`. Unticked means not allowed.

- [ ] The domain files (`encoding.lp`, `instance.lp`) may be changed.
- [ ] The UI may add or remove facts at runtime (`add_atom`/`remove_atom`).
- [ ] The UI may write files on the server (`download`).
- [ ] Technical/debug controls are wanted (e.g. explicit grounding buttons).
- [ ] Uploading `.lp` files through the UI is wanted.
- [ ] The explicitly documented custom backend operations in Part II §6 may be called.
- [ ] The quick-start files (`ui.lp` scaffold, `menu-bar.lp`) do **not** exist yet.

### 5. Preferences and expected result

**Layout or appearance:** [description, or "sensible defaults"]

**Must not be changed or added:** [list, or "none"]

**Files to return** (keep one):
`application section` (default) | `complete ui.lp` | `all changed/new files`

**How will you know it works?** (one or two concrete checks)
[Example: "After fixing Anna to room 1, room 2 no longer offers Anna, and
the status shows 'satisfiable'."]

### 6. Technical notes *(optional)*

[Known predicates, externals, optimization statements, or "none". For every
custom backend operation, give its exact operation term/signature, behavior,
state changes and domain-state predicates, error/atomicity behavior, backend
class or configuration, and required run-command options.]
~~~~
