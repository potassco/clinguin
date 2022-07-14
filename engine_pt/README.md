# Clinguin - Simple-Client-Server-Prototype

As the name suggests, this program is a prototype for Clinguin (an interactive-user-interface for Clingo). The program basically works as follows (for a full description see the corresponding development diary (`/project-document`): 

- Server:
    - Architecture wise, the server has a pretty standard layered-architecture
        - Presentation: Here the endpoints are located 
        - Application: Here the solver(s) is/are located
        - Data: Just the Data-Access-Objetcs (DAOs) for ClingoORM (CLORM)
    - Presentation: The server is basically a REST-server with two endpoints:
        - /health (GET) -> To check if the server is up and running
        - / (POST) -> Is a ''solver-function-caller'', e.g. if there exists a function ''f:X->Y'', then one may call it with argument ''1'' by passing a json string: `{ ''function'' : ''f(1)'' }`.

## Syntax

See the `/syntax_discussion/20220714_alex_syntax.lp` file.

## Starting:

### Whole-Application

`$ python start.py logic-program [... logic-program]`

E.g. for the sudoku example: `$ python start.py example/sudoku/instance.lp example/sudoku/encoding.lp example/sudoku/widgets.lp`

### Only Server

`$ python start_server.py logic-program [... logic-program]`

E.g. for the sudoku example: `$ python start_server.py example/sudoku/instance.lp example/sudoku/encoding.lp example/sudoku/widgets.lp`

### Only Client

`$ python start_client.py`

### Shutting down

Even though it is not the most ellegant way (and it will throw errors at you, so better hide), just `Ctr-C`.

