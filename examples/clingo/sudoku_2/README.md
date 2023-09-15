# Sudoku

The values that are inferred by the solver have a `*` appended.
Those that are part of a browsing solution are extended with `+`.

Start clinguin as an application:

```shell
clinguin client-server --frontend AngularFrontend --domain-files examples/clingo/sudoku_2/instance.lp examples/clingo/sudoku_2/encoding.lp --ui-files examples/clingo/sudoku_2/ui.lp
```

Or in the development environment:

```shell
python start.py server --domain-files examples/clingo/sudoku_2/instance.lp examples/clingo/sudoku_2/encoding.lp --ui-files examples/clingo/sudoku_2/ui.lp
```