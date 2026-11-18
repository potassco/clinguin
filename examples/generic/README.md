# Title

## Usage

Run the UI with the following command:

```console
clinguin share --ui-files ui.lp
```

## Table filters

Model, Assumptions, Brave, and Cautious have checkbox filters in their column
headers. Atom has no filter. Model, Brave, and Cautious offer Included and Not
included; Assumptions offers True, False, and No assumption.

No selected options means that column is unrestricted. Selected options within
a column are combined with OR; active filters across columns are combined with
AND. Assumed atoms remain candidates even when absent from the brave
consequences, but they must also match the active filters.

The shared dropdown rules use `row_name/1`, `row_header/3`, and `row_option/6`.
Filter selections use `filter_model/1`, `filter_assume/1`, `filter_brave/1`,
and `filter_cautious/1`.

## UI Inspect mode

```
clinguin share --inspect --build --ui-files examples/generic/ui.lp --domain-files examples/sudoku/encoding.lp examples/sudoku/instance.lp
```

## Assets

```
clinguin share --inspect --build --assets examples/generic/ \ --ui-files examples/generic/ui.lp \
  --domain-files examples/sudoku/encoding.lp examples/sudoku/instance.lp
```
