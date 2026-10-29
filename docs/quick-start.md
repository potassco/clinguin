# Quick start

Create a starting point for a Clinguin UI:

```console
clinguin init my-ui
cd my-ui
```

This creates:

```text
my-ui/
├── ui.lp
└── menu-bar.lp
```

The generated UI works without modification.

## Run the UI

Start the server and client together:

```console
clinguin share --ui-files ui.lp
```

Then open [http://0.0.0.0:8001/](http://0.0.0.0:8001/) in your browser.

## Generated files

### `ui.lp`

This is the main file for your application. It contains:

- the reusable template includes;
- the fixed application structure;
- an empty section for your application UI.

Add application elements below the `APPLICATION UI` comment and attach top-level content to `ui_content`.

For example:

```prolog
elem(welcome, div, ui_content).

    elem(welcome_text, span, welcome).
    attr(welcome_text, text, "Start building your UI here").
```

Do not rename or remove `ui_app` or `ui_content`. Templates use these elements as stable attachment points.

### `menu-bar.lp`

This file defines the reusable menu bar. It is included and enabled by default:

```prolog
#include "menu-bar.lp".
```

## Add an ASP encoding

When your application has a domain encoding and instance, pass them alongside the UI:

```console
clinguin share \
    --domain-files encoding.lp instance.lp \
    --ui-files ui.lp
```

Application-specific `elem/3`, `attr/3`, and `when/4` atoms can remain in `ui.lp` or be divided into additional files and included from there.

## Create files in the current directory

Omit the directory argument to initialize the current directory:

```console
clinguin init
```

Clinguin will stop if `ui.lp` or `menu-bar.lp` already exists. To deliberately replace those files, use:

```console
clinguin init --force
```

> !!! WARNING:
>     `--force` overwrites the existing quick-start files. Use it only when you do not need their current contents.
