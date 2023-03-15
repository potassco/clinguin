# Sudoku with explanations

Same sudoku but gives as options in the dropdown even those that lead to UNSAT.
If the user stects the, then the Unsat Core will light up to show why this is not available.


```shell
clinguin client-server --source-files examples/clingo/sudoku/instance.lp examples/clingo/sudoku/encoding.lp --ui-files examples/clingo/sudoku/ui.lp --include-menu-bar --assumption-signature=initial,3
```
