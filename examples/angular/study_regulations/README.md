# Study regulations

Create a study plan based on study regulations.

This encodings are used in the paper for study regulations in [ICLP 2024](https://www.iclp24.utdallas.edu/).


## Usage



```console
$ clinguin client-server --domain-files study_regulations/{encoding.lp,instance.lp} --ui-files study_regulations/ui.lp -c n=4
```

## UI

<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/study_regulations/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/study_regulations/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/study_regulations/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/study_regulations/ui.lp
  :language: prolog
  :caption: ui.lp
```
