# Tree Browser

- **Backend**:   `ClingraphBackend`

An advanced integration with clingraph where the style of the clingraph nodes is updated using the UI.

Notice that web browser might need to be resized to see the clingraph image.

## Usage

```console
$ clinguin client-server --domain-files tree_browser/{encoding.lp,instance.lp} --ui-files tree_browser/ui.lp --backend=ClingraphBackend --clingraph-files tree_browser/viz.lp
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/tree_browser/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/tree_browser/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/tree_browser/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/tree_browser/ui.lp
  :language: prolog
  :caption: ui.lp
```

