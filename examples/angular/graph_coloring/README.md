# Graph coloring

- **Backend**:   `ClingraphBackend`

Implements the [graph coloring problem](https://en.wikipedia.org/wiki/Graph_coloring). Showcases how to use the domain state in the *clingraph* encoding.


## Usage

```console
$ clinguin client-server --domain-files graph_coloring/{encoding.lp,instance.lp} --ui-files graph_coloring/ui.lp --backend=ClingraphBackend --clingraph-files=graph_coloring/viz.lp
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/graph_coloring/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/graph_coloring/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/graph_coloring/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/graph_coloring/ui.lp
  :language: prolog
  :caption: ui.lp
```
