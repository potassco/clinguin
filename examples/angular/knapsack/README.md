# Knapsack

Solves the [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem).
By doing so, it showcases the use of optimal consequences and false assumptions as well as drag and drop.

For a version with the option to lock and unlock drag and drop, check the commented code.

## Usage

```console
$ clinguin client-server --domain-files knapsack/{encoding.lp,instance.lp} --ui-files knapsack/ui.lp
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/knapsack/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/knapsack/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/knapsack/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/knapsack/ui.lp
  :language: prolog
  :caption: ui.lp
```

