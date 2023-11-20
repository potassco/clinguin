## Tree Browser

- **Backend**:   `ClingraphBackend`
- **Frontend**:   `AngularFrontend`

An advanced integration with clingraph where the style of the clingraph nodes is updated using the UI

Notice that web browser might need to be resized to see the clingraph image.

### Usage

```
clinguin client-server --frontend AngularFrontend --domain-files examples/angular/tree_browser/encoding.lp examples/angular/tree_browser/instance.lp --ui-files examples/angular/tree_browser/ui.lp   --backend=ClingraphBackend --clingraph-files=examples/angular/tree_browser/viz.lp
```

![](out1.png)
![](out2.png)
![](out3.png)
![](out4.png)
