# Clinguin :penguin: 

Simple-Client-Server-Prototype

As the name suggests, this program is a prototype for Clinguin (an interactive-user-interface for Clingo). The program basically works as follows (for a full description see the corresponding development diary (`/project-document`): 

- Server:
    - Architecture wise, the server has a pretty standard layered-architecture
        - Presentation: Here the endpoints are located 
        - Application: Here the solver(s) is/are located
        - Data: Just the Data-Access-Objetcs (DAOs) for ClingoORM (CLORM)
    - Presentation: The server is basically a REST-server with two endpoints:
        - /health (GET) -> To check if the server is up and running
        - / (POST) -> Is a ''solver-function-caller'', e.g. if there exists a function ''f:X->Y'', then one may call it with argument ''1'' by passing a json string: `{ ''function'' : ''f(1)'' }`.

## Install

- Python (version 3.8, 3.9, or 3.10)


```
pip install . -e
```


## Syntax

See the `/syntax_discussion/20220714_alex_syntax.lp` file.

## Starting:

### Whole-Application

`$ clinguin start.py client-server [--solver=solver] logic-program [... logic-program] --solver solver-library`

E.g. for the sudoku example: `$ clinguin examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

Or to specify the solver: `$ python start.py examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp --solver server.application.standard_solver.StandardSolver`

### Only Server

`$ python start.py server [--solver=solver] logic-program [... logic-program]`

E.g. for the sudoku example: `$ python start_server.py examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

### Only Client

`$ python start.py client`

### Shutting down

Even though it is not the most ellegant way (and it will throw errors at you, so better hide), just `Ctr-C`.

## Dependencies:

All dependencies can be installed via `pip install XYZ` 

- Server:
    - json
    - pydantic
    - typing
    - clingo
    - clorm
    - networkx
    - fastapi
    - uvicorn
- Client:
    - time
    - json
    - tkinter
    - httpx



## Implementation of own Solver

Preliminary 1: This section will be expanded in the future.

Preliminary 2: Standard behavior: The standard behavior is to load the solver in the package `server.application.standard_solver.StandardSolver`. This solver will get instanciated by default, therefore when one wants to specify another solver, one needs to add the `--solver` argument-option and then specify the package where the solver is located.

Implementation: For the implementation of one's own solver, one basically has free hands in terms of syntactic definitions of the class, except two (or three) things:
1. The `__init__()` method takes an argument `logic_programs` which is a list of string-paths to the logic programs (the existance of the files has been checked by now, but not the content).
2. When a method needs to return something to the client/User-Interface (UI) the method must return a **Json-convertible-class-hierarchy**. If one uses the standard-UI it is highly recommended to use the `ElementDto`, `AttributeDto` and `CallbackDto` classes to save the class hierarchy, otherwise one needs to at least implement the functionality of the `ElementDto` class and further provide a `root` element (initialized with the default `ElementDto` by `ElementDto('root', 'root', 'root')`). 
3. If one uses the **standard-UI** then one needs to provide a `solve()` method in the solver. This method takes no argument and returns a json-convertible class hierarchy. This is needed, as the solve() method is initially invoked by the UI.



## Implementation of own Client/User-Inteface (UI)

### Extending the Python-UI

For this one needs to implement a class which is a subtype of the `AbstractGui` (`client.presentation.abstract_gui.AbstractGui`) class. It is recommended to do this in a folder next to the `tkinter` folder/package (`client.presentation.tkinter`). E.g. the class `client.presentation.custom_gui.fancy_gui.FancyGui`. For the implementation one needs to implement the behavior of the syntax specification (`20220714_alex_syntax.lp`).

The next thing to do is to invoke the GUI, by changing a line in the class `client.application.client_base.ClientBase`. This line is the creation of the `TkinterGui()` object, so the line: `self.gui_generator = TkinterGui(self)`, with ones own fancy gui, like `self.gui_generator = FancyGui()`.



































