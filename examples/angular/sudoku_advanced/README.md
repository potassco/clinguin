## Sudoku

- **Backend**:   `ExplanationBackend`
- **Frontend**:   `AngularFrontend`

An advanced version of the sudoku where all values are listed as possibilities but when an invalid one is chosen, the explanation is highlighted

### Usage

```
clinguin client-server --frontend AngularFrontend --domain-files examples/angular/sudoku_advanced/instance.lp examples/angular/sudoku_advanced/encoding.lp --ui-files examples/angular/sudoku_advanced/ui.lp --backend ExplanationBackend  --assumption-signature initial,3
```

![](out1.png)
![](out2.png)
![](out3.png)
