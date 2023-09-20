# Housing 2

You must select the people and then divide into rooms.
Includes the option to browse optimal solutions in order and uses a pre=made menu bar


Start clinguin as an application:

```shell
clinguin client-server --frontend AngularFrontend --domain-files examples/clingo_web/acomodation/instance.lp examples/clingo_web/acomodation/encoding.lp --ui-files examples/clingo_web/acomodation/ui.lp
```

Or in the development environment:

```shell
python start.py server --domain-files examples/clingo_web/acomodation/instance.lp examples/clingo_web/acomodation/encoding.lp --ui-files examples/clingo_web/acomodation/ui.lp
```
