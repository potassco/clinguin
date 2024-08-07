.. clinguin documentation master file,  created by
   sphinx-quickstart on Wed Aug 31 12:21:45 2022.
   You can adapt this file completely to your liking,  but it should at least
   contain the root `toctree` directive.

Clinguin: Building UIs in ASP
=========================================

Clinguin enables ASP developers to create interactive User Interface (UI) prototypes using only ASP.
UIs are defined as sets of facts,  which are then rendered by a fronted to provide continuous interaction with ASP solvers based on user-triggered events.

- :ref:`Quick Start`: Step-by-step guide on how to use clinguin using the sudoku.
- :ref:`Reference Guide`: Explanation of the concepts and components of clinguin.
- :ref:`Frontends`: Elements and attributes available to crate your UI.
- :ref:`Backends`: Available operations and the predicates that will be available to create the UI.
- :ref:`Customization`: Create your own backend or contribute with the *clinguin* project.
- :ref:`Help`: If you are having trouble.
- :ref:`Examples`: To get inspiration for your UI.

**Here is a motivation example:**

Consider an ASP encoding that solves the sudoku puzzle where cells are defined by prediate  ``pos(X,Y)`` and solutions by ``sudoku(X,Y,V)``
clinguin will use this encoding and the following UI encoding to construct the UI shown bellow.

.. code-block::

  elem(window, window, root).
  attr(window, child_layout, grid).
  attr(window,class,("justify-content-start")).

    elem(dd(X,Y), dropdown_menu, window) :- pos(X,Y).
    attr(dd(X,Y), width, 50)  :- pos(X,Y).
    attr(dd(X,Y), height, 50) :- pos(X,Y).
    attr(dd(X,Y), grid_column, X) :- pos(X,Y).
    attr(dd(X,Y), grid_row, Y) :- pos(X,Y).
    attr(dd(X,Y), class, ("border-dark";"bg-primary")) :- pos(X,Y).
    attr(dd(X,Y), class, "bg-opacity-50") :- subgrid(X,Y,S),  S\2!=0.
    attr(dd(X,Y), selected, V) :- _all(sudoku(X,Y, V)).

        elem(ddv(X,Y, V), dropdown_menu_item, dd(X,Y)) :- _any(sudoku(X,Y, V)).
        attr(ddv(X,Y, V), label, V) :- _any(sudoku(X,Y, V)).
        when(ddv(X,Y, V), click, call, add_assumption(sudoku(X,Y, V))) :- _any(sudoku(X,Y, V)).



.. image:: ../examples/angular/elevator/ui.gif


.. note:: Clinguin is part of the `Potassco umbrella <https://potassco.org/>`_ (which is the home of Clingo and the other ASP tools)

.. toctree::
   :hidden:

   clinguin/installation
   clinguin/use
   clinguin/reference/index
   clinguin/frontends/index
   clinguin/backends/index
   clinguin/development/index
   clinguin/examples/index
   clinguin/help



