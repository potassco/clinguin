# Placement

Showcases multiple features of the web fronted in the form of a smart seat placement application.

This example show how to use consequences with optimization statements to have user feedback on optimal models.
The option ` --opt-timeout 0` makes sure that one model is computed at a time to try to find the optimal one.

## Usage

```
clinguin client-server --domain-files placement/{instance.lp,encoding.lp} --ui-files placement/ui.lp --opt-timeout 0
```

## UI

<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/placement/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/placement/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/placement/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/placement/ui.lp
  :language: prolog
  :caption: ui.lp
```




