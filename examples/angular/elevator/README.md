# Elevator

This example showcases one way to use clinguin in an incremental multi-shot encoding. In this case we use a planning problem of an elevator.

## Usage

```console
$ clinguin client-server --domain-files elevator/{encoding.lp,instance.lp} --ui-files elevator/ui.lp
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/elevator/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/elevator/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/elevator/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/elevator/ui.lp
  :language: prolog
  :caption: ui.lp
```



