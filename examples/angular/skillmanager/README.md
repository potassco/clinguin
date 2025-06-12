# Skill manager


This example uses a toy example of managing and mastering skills to
showcase the use of collapse components, side bar, and file managing.

## Usage

```console
$ clinguin client-server --domain-files skillmanager/encoding.lp --ui-files skillmanager/ui.lp  --optional-files skillmanager/instance_programming.lp
```

No instance will be available at the start but the `skillmanager/instance_programming.lp` can be activated in the sidebar.
Furthermore, one can upload other instances defining skills using the file upload.


## Domain Files

```{literalinclude} ../../../examples/angular/skillmanager/encoding.lp
  :language: prolog
  :caption: encoding.lp
```

## Optional Files

```{literalinclude} ../../../examples/angular/skillmanager/instance_hobby.lp
  :language: prolog
  :caption: instance_hobby.lp
```

```{literalinclude} ../../../examples/angular/skillmanager/instance_programming.lp
  :language: prolog
  :caption: instance_programming.lp
```

## UI Files

```{literalinclude} ../../../examples/angular/skillmanager/ui.lp
  :language: prolog
  :caption: ui.lp
```
