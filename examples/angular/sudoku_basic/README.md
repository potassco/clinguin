# Sudoku

This example uses the well known [sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku) to showcase most basic feature of clinguin.


## Usage

```console
$ clinguin client-server --domain-files sudoku_basic/{encoding.lp,instance.lp} --ui-files sudoku_basic/ui.lp
```

## UI

<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/sudoku_basic/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/sudoku_basic/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/sudoku_basic/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/sudoku_basic/ui.lp
  :language: prolog
  :caption: ui.lp
```


