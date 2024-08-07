# Sudoku Explained

- **Backend**:   `ExplanationBackend`

An advanced version of the sudoku where all values are listed as possibilities but when an invalid one is chosen, the explanation is highlighted.

Notice that the instances uses choices on predicate `initial/3`. This way they can be used as assumptions and be included in the `_clinguin_mus` predicate by the `ExplanationBackend`. The option `--assumption-signature initial,3` adds all these atoms as true assumptions.


## Usage

```console
$ clinguin client-server --domain-files sudoku_advanced/{encoding.lp,instance.lp} --ui-files sudoku_advanced/ui.lp --backend ExplanationBackend  --assumption-signature initial,3
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/sudoku_advanced/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/sudoku_advanced/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/sudoku_advanced/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/sudoku_advanced/ui.lp
  :language: prolog
  :caption: ui.lp
```


