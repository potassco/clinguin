# Sudoku

This example uses the well known [sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku).


## Usage

```console
$ clinguin client-server --domain-files sudoku/{encoding.lp,instance.lp} --ui-files sudoku/ui.lp
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/sudoku/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/sudoku/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/sudoku/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/sudoku/ui.lp
  :language: prolog
  :caption: ui.lp
```


