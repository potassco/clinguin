# Jobshop

- **Backend**:   `ClingoDLBackend`

This example is a simple version of the [job-shop scheduling problem](https://en.wikipedia.org/wiki/Job-shop_scheduling) which uses [clingodl](https://potassco.org/labs/clingoDL/).

## Usage

```console
$ clinguin client-server --domain-files jobshop/encoding.lp  jobshop/instance.lp --ui-files jobshop/ui.lp  --backend ClingoDLBackend
```



<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/jobshop/ui.gif?raw=true">

## Domain Files

```{literalinclude} ../../../examples/angular/jobshop/instance.lp
  :language: prolog
  :caption: instance.lp
```
```{literalinclude} ../../../examples/angular/jobshop/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/jobshop/ui.lp
  :language: prolog
  :caption: ui.lp
```
