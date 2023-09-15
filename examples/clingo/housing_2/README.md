# Housing 2

You must select the people and then divide into rooms.
Includes the option to browse optimal solutions in order and uses a pre=made menu bar


Start clinguin as an application:

```shell
clinguin client-server --frontend AngularFrontend --domain-files examples/clingo/housing_2/instance.lp examples/clingo/housing_2/encoding.lp --ui-files examples/clingo/housing_2/ui.lp --include-menu-bar
```

Or in the development environment:

```shell
python start.py server --domain-files examples/clingo/housing_2/instance.lp examples/clingo/housing_2/encoding.lp --ui-files examples/clingo/housing_2/ui.lp --include-menu-bar
```
