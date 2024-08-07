# Cats and dogs

- **Backend**:   `ExplanationBackend`

This example was used in the paper for clinguin in [ICLP 2024](https://www.iclp24.utdallas.edu/).
The aim is to place people in tables so that no cat-people are sitting with dog-people.

[GitHub source code](https://github.com/potassco/clinguin/blob/gifs/examples/angular/catdog)

## Usage

```console
$ clinguin client-server --domain-files examples/angular/catdog/{instance.lp,encoding-explain.lp} --ui-files examples/angular/catdog/{ui-tables.lp,ui-menu.lp,ui-people.lp,ui-explain.lp,ui-explain-msg.lp} --backend ExplanationBackend --assumption-signature cons,2
```

## UI

<img src="https://github.com/potassco/clinguin/blob/gifs/examples/angular/catdog/ui.gif?raw=true" height="100">

## Domain Files

```{literalinclude} ../../../examples/angular/catdog/instance.lp
  :language: prolog
  :caption: instance.lp
```

```{literalinclude} ../../../examples/angular/catdog/encoding-explain.lp
  :language: prolog
  :caption: encoding-explain.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/catdog/ui-tables.lp
  :language: prolog
  :caption: ui-tables.lp
```

```{literalinclude} ../../../examples/angular/catdog/ui-menu.lp
  :language: prolog
  :caption: ui-menu.lp
```

```{literalinclude} ../../../examples/angular/catdog/ui-people.lp
  :language: prolog
  :caption: ui-people.lp
```

```{literalinclude} ../../../examples/angular/catdog/ui-explain.lp
  :language: prolog
  :caption: ui-explain.lp
```

```{literalinclude} ../../../examples/angular/catdog/ui-explain-msg.lp
  :language: prolog
  :caption: ui-explain-msg.lp
```