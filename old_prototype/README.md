# Clinguin :penguin:

## Goal

A framework to design interactive UIs using clingo. 

- UIs are defined by facts
- UIs are rendered using some backend
  - We are using [tkinter](https://docs.python.org/3/library/tkinter.html) at the moment.
  - We might want to provide different backends, such as ipwidgets

## Requirements

- clingo 
- clorm
- networkx
- tkinter

## Usage

Example with sudoku:

The following command will open a window defined via [`examples/sudoku/widgets.lp`](examples/sudoku/widgets.lp)

```
python clinguin.py examples/sudoku/encoding.lp examples/sudoku/widgets.lp examples/sudoku/instance.lp
```

## Basic prototype

This is a very simple prototype so the code is not optimized or modularized. 

### The layout and widgets

The UI layout is defined based on the cautions model with the following predicates:

#### Window configuration

```
window(FUNCTION,ARG,VALUE).
```

calls the function `FUNCTION` using argument `ARG` and value `VALUE`

```python
w = Tk()
w.FUNCTION(ARG=VALUE)
```

if `ARG` is a number is the position of the argument in the call, otherwise is a keyword argument


#### Widget creation


```
widget(TYPE,ID,PARENT).
```

crates a widget of type `TYPE` (`menu`,`frame`) with an identifier `ID` and a parent `PARENT` which can be an id of another widget or `window`.

#### Widget location

```
geo(ID,TYPE,ARG,VALUE)
```

Uses the geometry manager `TYPE` (`grid`,`place`,`pack`) on  the widget `ID` passing the argument and value.

#### Widget configuration

```
config(ID,ARG,VALUE)
```

Configures the widget `ID` by passing the argument and value.

### The widgets options

The UI options are defined based on the appearance of the following predicate in the brave model

```
opt(ID,VAL,SYMBOL)
```

Adds an option with value `VAL` to the widget `ID` that asserts the symbol `SYMBOL` when it is selected.



