# Clinguin :penguin: 

Clinguin is a graphical-user-interface for Clingo, where one can specify the user-interface entirely in a logic-program. One might wonder how one can do this by him-/herself - for this see the descriptions below and have fun :-)

## Install

Preliminaries:
- Python (version 3.8, 3.9, or 3.10)

Now clone the repository, and move to the repository. In the repo you should see a `setup.py` file. Now execute the following command:

```
python setup.py install
```

Now `STAY` in this directory, as currently (see issue #61 on GitHub) there is a bug, where one can only execute clinguin from this location.

## The first example

After the installation, executing the first example is quite straightforward, just copy-paste the following command into your commandprompt:

`clinguin client-server examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

After you hit enter, a Sudoku-game should open, which you can play - have fun :-)

## Next Steps

Next steps - now it is time for you to try out some stuff yourself. In the folder(s) `exapmles` you find some smaller and some bigger example programs, which you can take as a first stepping stone for building your own Clingo-Frontend.

### Syntax

For the development it is useful to know which elements, attribute-keys and -values are available. For this you can hit: `clinguin client --gui-syntax` for an overview and `clinguin client --gui-syntax-full` for a detailed list and description of the available widgets.

### Help

Clinguin is divided into three different sub-programs: Client, Server and Client-Server. One can access the help section of each one of those individually, i.e.:
- `clinguin client -h`
- `clinguin server -h`
- `clinguin client-server -h`

## Starting/Installation-2:

The following section provides more details about installation and execution, in general there are two start-possibilities:
1. Package-Version
2. Development-Version

### Package-Version

For the package version one must first install `clinguin`, then execute it.

#### Installation

- If `make` is installed, just hit `make`
- Otherwise `python setup.py install`

After the installation a package with the name `clinguin` should have been installed. One can test this by hitting `clinguin -h`, to see the help. 

#### Deinstallation

`pip uninstall clinguin`

#### Standard-Start

See `$ clinguin client-server -h`

`$ clinguin client-server [--custom-server-classes=folder-path] [--custom-client-classes=folder-path] [--solver=solver] [--client=client] logic-program [... logic-program]`

- custom-client/server-classes: Specify the folder, where the solver(s) are located.
- solver/client: Specify the solver/client, which must be in the folder (or subfolder) where custom-classes points to - Pro-Tip: See which solvers/clients are available by typing: `clinguin client-server -h`
- 

E.g. for the sudoku example: `$ clinguin client-server examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

Or to specify the solver: `$ clinguin client-server --custom-server-classes='./clinguin/server/application/default_backends' --solver=ClingoBackend examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

#### Only Server 

See `$ clinguin server -h`

`$ clinguin server  [--custom-server-classes=folder-path] [--solver=solver] logic-program [... logic-program]`


E.g. for the sudoku example: `$ clinguin server examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

#### Only Client

See `$ clinguin client -h`

`$ clinguin client [--custom-client-classes=folder-path] [--client=client] `


#### Shutting down

Even though it is not the most ellegant way (and it will throw errors at you, so better hide), just close the GUI first and then hit `Ctr-C`.

### Development-Version

#### Standard-Start

See `$ python start.py client-server -h`

`$ python start.py client-server [--custom-classes=folder-path] [--solver=solver] logic-program [... logic-program]`

E.g. for the sudoku example: `$ python start.py examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

Or to specify the solver: `$ python start.py client-server --custom-classes='./clinguin/server/application/default_backends' --solver=ClingoBackend examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

#### Only Server

See `$ python start.py server -h`

`$ python start.py server [--solver=solver] logic-program [... logic-program]`

E.g. for the sudoku example: `$ python start_server.py examples/sudoku/instance.lp examples/sudoku/encoding.lp examples/sudoku/widgets.lp`

#### Only Client

See `$ python start.py client -h`

`$ python start.py client`

#### Shutting down

Do the following for:
- `client` and `client-server`: Close at FIRST the GUI-Window and then press `Ctrl-C`
- `server`: Just press `Ctrl-C`

## Dependencies:

All dependencies can be installed via `python setup.py install` 

## Implementation of own Solver

Preliminary 1: This section will be expanded in the future.

Preliminary 2: Standard/Default behavior: The standard behavior is to load the solver in the package `server.application.clingo_backend.StandardSolver`. This solver will get instanciated by default, therefore when one wants to specify another solver, one needs to add the `--solver` argument-option and then specify the package where the solver is located.

Implementation: For the implementation of one's own solver, one basically has free hands in terms of syntactic definitions of the class, except two (or three) things:
1. The `__init__()` method takes an argument `args` which are the command-line arguments (see `clinguin/server/application/default_backends/clingo_backend.py`) 
2. When a method needs to return something to the client/User-Interface (UI) the method must return a **Json-convertible-class-hierarchy**. If one uses the standard-UI it is highly recommended to use the `ElementDto`, `AttributeDto` and `CallbackDto` classes to save the class hierarchy, otherwise one needs to at least implement the functionality of the `ElementDto` class and further provide a `root` element (initialized with the default `ElementDto` by `ElementDto('root', 'root', 'root')`). 
3. One needs to provide a `get()` method in the solver. This method takes no argument and returns a json-convertible class hierarchy. This is needed, as this method is initially invoked by the UI.

## Implementation of own Client/User-Inteface (UI)

### Extending the Python-UI

For this one needs to implement a class which is a subtype of the `AbstractFrontend` (`client.presentation.abstract_frontend.AbstractFrontend`) class. It is recommended to do this in a folder next to the `tkinter` folder/package (`client.presentation.tkinter`). E.g. the class `client.presentation.custom_frontend.fancy_frontend.FancyFrontend`. For the implementation one needs to implement the behavior of the syntax specification (`20220714_alex_syntax.lp`).

The next thing to do is to invoke the GUI, by changing a line in the class `client.application.client_base.ClientBase`. This line is the creation of the `TkinterFrontend()` object, so the line: `self.frontend_generator = TkinterFrontend(self)`, with ones own fancy gui, like `self.frontend_generator = FancyFrontend()`.

## Other examples:

### Elevator:

Is located in: `examples/elevator` - can be executed by:

`$ clinguin client-server --custom-server-classes='./examples/elevator' --solver=TemporalBackend --source-files=examples/elevator/encoding.lp --widget-files=examples/elevator/widgets.lp`

# Linting:

`<PATH>/clinguin$ pylint --disable=C0301,C0303,C0305,R1705,W0703,R0201,W0707,W0122,C0116,W0622,C0103,R0903,W0401,W0614 clinguin`































