This example generates an ASP-graph of a simple 3 color program (which can be found in the clingraph 3color example). 
The graph can be revealed bit by bit by using the "show_children" option on the variozs nodes. 
The example can be run with the following command:

```shell
python start.py client-server --backend=ClingraphInteractiveBackend --program examples/clingraph_interactive/clingraph_interactive_ASP/program.lp --viz-encoding examples/clingraph_interactive/clingraph_interactive_ASP/encoding.lp --options-encoding examples/clingraph_interactive/clingraph_interactive_ASP/options-encoding.lp --user-input-encoding examples/clingraph_interactive/clingraph_interactive_ASP/user-encoding.lp --frontend AngularFrontend
```

Afterwards, type localhost:4200 into your browser. 
