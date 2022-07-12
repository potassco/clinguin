Start the prototype via: `python start_application.py examples/sudoku/widgets.lp`

Then a server should open at `127.0.0.1:8000`. Test it via a post request on `http://127.0.0.1:8000` with the Json-Body-Content: `{ "function" : "solve", "arguments" : [] }`.
