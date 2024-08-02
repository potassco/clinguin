## Placement

- **Backend**:   `ClingoMultishotBackend`
- **Frontend**:   `AngularFrontend`

This example show how to use consequences with optimization statements to have user feedback on optimal models.

The option ` --opt-timeout 0` makes sure that one model is computed at a time to try to find the optimal one.

### Usage

```
clinguin client-server --domain-files examples/angular/placement_optimized/instance.lp examples/angular/placement_optimized/encoding.lp --ui-files examples/angular/placement_optimized/ui.lp  --opt-timeout 0
```

![](out1.png)
![](out2.png)
![](out3.png)
