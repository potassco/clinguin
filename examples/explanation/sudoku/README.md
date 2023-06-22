# Sudoku with explanations

Same sudoku but gives as options in the dropdown even those that lead to UNSAT.
If the user selects the, then the Unsat Core will light up to show why this is not available.
The `ignore-unsat-msg` flag is necessary to exclude the usual way of handling UNSAT outputs via a pop-up message to the user


```shell
clinguin client-server --domain-files examples/clingo/sudoku/instance.lp examples/clingo/sudoku/encoding.lp --ui-files examples/clingo/sudoku/ui.lp --include-menu-bar --assumption-signature=initial,3 --ignore-unsat-msg
```
