# Clinguin

Clinguin enables ASP developers to **create interactive User Interface** (UI) prototypes **using only ASP**.
UIs are defined as sets of facts,  which are then rendered by a fronted to provide continuous interaction with ASP solvers based on user-triggered events.

***Your UI definition would look like this!***

```prolog
elem(w, window, root).
elem(b1, button, w).
attr(b1, label, "Button 1").
when(b1, click, call, next_solution).
```

### Usage

Look at our [documentation page](https://clinguin.readthedocs.io/en/latest/) to see how to use clinguin.

### Examples

Our **[examples folder](https://github.com/potassco/clinguin/tree/master/examples)** shows how to use the range of functionalities in different applications.

<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/placement/out1.png?raw=true" height="150">
<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/graph_coloring/out2.png?raw=true" height="150">
<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/sudoku/out1.png?raw=true" height="150">
<img src="https://github.com/potassco/clinguin/blob/master/examples/angular/jobshop/out.png?raw=true" height="150">


### Extensions

***Integration with different applications***

Clinguin includes a wide range of [clingo](https://potassco.org/clingo/) functionalities such as multi-shot solving, theory solving and more! It also has extensions for interacting with [clingraph](https://clinguin.readthedocs.io/en/latest/clinguin/installation.html) graphs and providing explanations.


***Is clinguin missing something for your application?***

No worries! Clinguin can be extended with different functionalities and even frontend languages, take a look [at this guide](https://clinguin.readthedocs.io/en/latest/clinguin/backends.html#creating-your-own-backend).


## Installation

### Requirements

- Python (version 3.8, 3.9, or 3.10)

For instructions to install from source, pip and conda see our [documentation page](https://clinguin.readthedocs.io/en/latest/clinguin/installation.html).
