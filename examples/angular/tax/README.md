# Tax

- **Backend**:   `FclingoBackend`

This example calculates the tax using fclingo

## Usage

```console
$ clinguin client-server --domain-files tax/encoding.lp  tax/instance.lp --ui-files tax/ui.lp   --backend FclingoBackend
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/tax/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/tax/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/tax/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/tax/ui.lp
  :language: prolog
  :caption: ui.lp
```
