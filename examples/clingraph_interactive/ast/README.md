This example generates an ASP-graph of a simple 3 color program (which can be found in the clingraph 3color example). 
The graph can be revealed bit by bit by using the "show_children" option on the variozs nodes. 
The example can be run with the following command:

Start clinguin as an application:

```shell
clinguin client-server --frontend AngularFrontend --backend=ClingraphBackend --domain-files examples/clingraph_interactive/ast/domain_file.lp --ui-files examples/clingraph_interactive/ast/ui.lp --clingraph-files=examples/clingraph_interactive/ast/clingrah_encoding.lp
```

Or in the development environment:


```shell
python start.py server --domain-files examples/clingraph_interactive/ast/domain_file.lp --ui-files examples/clingraph_interactive/ast/ui.lp   --backend=ClingraphBackend --clingraph-files=examples/clingraph_interactive/ast/clingrah_encoding.lp
```

Afterwards start the clinguin web-frontend and type localhost:4200 into your browser. 
