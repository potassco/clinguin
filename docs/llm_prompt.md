# Generate a UI with an LLM

You can use the following prompt with an LLM to generate a Clinguin UI from an ASP encoding and a short description.

Before using the prompt:

1. Create a quick-start project with `clinguin init my-ui`.
2. Edit only the `USER INPUT` section at the beginning of the prompt.
3. Paste your domain encoding there or attach the domain files to the LLM.
4. Attach `ui.lp` or `menu-bar.lp` only if you have already customized them.
5. Copy the complete prompt and send it to the LLM.
6. Paste the generated application code below `APPLICATION UI` in `ui.lp`.

> LLM-generated code may use components or backend operations that Clinguin
> does not support. Review the output before using it.

## Prompt

~~~~text
# USER INPUT — EDIT ONLY THIS SECTION

## Application

Purpose:
[Describe the application in a few sentences.]

User workflow:
[Describe what the user should select, enter, inspect, or trigger.]

Required controls:
[List buttons, forms, selections, status information, solver actions, etc.]

Layout and appearance:
[Describe the preferred layout and visual style, or write "choose sensible defaults".]

Additional requirements:
[List anything else, or write "none".]

## Domain encoding

--- BEGIN DOMAIN ENCODING ---

[Paste the encoding here, or write "attached as encoding.lp".]

--- END DOMAIN ENCODING ---

## Instance

[Paste the instance here, write "attached", or write "none".]

## Existing custom UI

The project should normally be initialized with:

    clinguin init my-ui

If `ui.lp` or `menu-bar.lp` has already been customized, paste it here or
attach it to the LLM. Otherwise write `standard quick-start files`.

--- BEGIN EXISTING UI ---

standard quick-start files

--- END EXISTING UI ---

# END USER INPUT — DO NOT EDIT BELOW


# TASK

You are creating a user interface for Clinguin v3.

Generate valid Clinguin UI code based on the user input above. Do not generate
JavaScript, TypeScript, Svelte, HTML files, or Python unless the user explicitly
requests a custom backend or frontend component.

Assume the standard quick-start files already define `ui_app` and `ui_content`
and include `menu-bar.lp`. Generate application-specific code to place below
the `APPLICATION UI` comment in `ui.lp`.

If customized UI files were supplied, preserve their structure. Do not rename
or redefine `ui_app`, `ui_content`, or the menu-bar insertion points.

## Authoritative sources

Clinguin v3 is currently under development. The default `master` branch and
the published Clinguin documentation describe v2. Do not use them as a source
for v3 frontend components, backend APIs, or command-line behavior.

Use the current v3 development source for implementation details:

https://github.com/potassco/clinguin/tree/examples/mm

Relevant v3 source locations:

- src/clinguin/client/svelte/src/lib/resolveComponent.ts
- src/clinguin/client/svelte/src/lib/frontendElement.ts
- src/clinguin/client/svelte/src/lib/components/
- src/clinguin/server/domain_state.py
- src/clinguin/server/backends/clingo_backend.py

The v2 reference may be used only for the general principles of how Clinguin
connects domain encodings, domain state, UI encodings, the server, and the
client. These principles remain broadly applicable to v3:

https://github.com/potassco/clinguin/tree/6f4e51d89b89a51518ccacd05efca2a722aa739a/docs/clinguin/reference

Do not copy element types, frontend components, backend lists, operations,
commands, or API details from the v2 reference. Verify those against the v3
source.

When versioned v3 documentation and a v3 release are available, prefer the
documentation and source tag matching the user's installed version over all
development and v2 links above.

External visual references:

- shadcn-svelte components:
  https://www.shadcn-svelte.com/docs/components
- Tailwind CSS:
  https://tailwindcss.com/docs/styling-with-utility-classes
- Lucide icons:
  https://lucide.dev/icons/

External component documentation is visual inspiration. It does not prove
that a component is exposed through Clinguin's `elem/3` interface.

If the documentation and source cannot be accessed, follow this minimum
compatibility contract:

- Construct the UI with `elem/3`, `attr/3`, and `when/4`.
- Attach application content to `ui_content`.
- Treat `root` as the reserved root parent.
- Use native HTML elements or components verified in Clinguin v3.
- Do not use the obsolete v2 types `window` or `container`.
- Use Tailwind classes through `attr(ID, class, VALUE)`.
- Use only documented backend operations and domain-state predicates.
- Do not invent components, predicates, or operations.
- Indent nested atoms so that the element hierarchy is visible.

## Output requirements

Return:

1. A short explanation of the proposed UI structure.
2. The complete application section to add to ui.lp.
3. Changes to menu-bar.lp only if they are necessary.
4. Any additional .lp files, each in a separate code block with its filename.
5. The command needed to run the result.
6. A short list of assumptions or required custom backend operations.

The generated code must satisfy all of the following:

- Valid ASP syntax with periods after every fact and rule.
- Only elem/3, attr/3, and when/4 for UI construction.
- Unique element IDs.
- Every parent exists.
- No window or container element types.
- No invented Clinguin components.
- No invented backend operations.
- Application content is attached to ui_content.
- Menu actions use menubar_left, menubar_center, or menubar_right when the
  quick-start menu bar is present.
- The supplied domain encoding is not modified unless I explicitly request it.
- Conditional UI rules use predicates that actually exist in the supplied
  encoding or documented Clinguin domain state.
- The result works without requiring custom frontend code unless that need is
  explicitly identified.

Ask no more than three short clarification questions if essential information
is missing. Otherwise, choose sensible defaults and generate the UI.

~~~~

## Running the generated UI

Save the generated application code in `ui.lp`, then run:

```console
clinguin share \
    --domain-files encoding.lp instance.lp \
    --ui-files ui.lp
```
