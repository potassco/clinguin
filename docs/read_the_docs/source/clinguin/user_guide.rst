User Guide
##########

This guide is for the people, who want to get to know how `clinguin` works.
It assumes `clinguin` has already been installed es described in :ref:`Installation`

Mechanics
=========

The `clinguin` system uses a Client-Server Architecture, thus it is separated into two processes. 

* **Server**: Will run a clingo process in the background and generate a UI specification based on a UI encoding and a domain specific encoding. It will then wait for notifications by the client to interact with the clingo process trough the *Backend*.

* **Client**: Will ask the server for the information to render the UI with the selected *Frontend*. Then send the information corresponding to the user selection back to the server.

To allow flexibility, further separation is done to have interchangeable Backends and Frontends.

* **Backend**: Will define the control and functionality that is available. The backend will start the clingo solving process and manage the encoding and the ui. The user can create their own Backend to increase functionality (See the :ref:`customize_guide` for more information). We provide the following `Backends <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/default_backends>`_ with the system:

    * *ClingoBackend*: Basic clingo functionality
    * *ClingraphBackend*: Basic clingo functionality with the option to render clingraph images on the side
    * *TemporalBackend*: Basic temporal functionalities
    * *ExplanationBackend*: Basic explanation functionalities

* **Frontend**: Will generate the layout based on a JSON and display the UI. The user can create their own Frontend to have a different view (See the :ref:`customize_guide` for more information).  the following Frontends with the system:

    * *Tkinter*: UI using the well known tkinter interface


Basic Usage
===========

We can run a first example: **Sudoku**. 
All files used can be find `here <https://github.com/krr-up/clinguin/tree/master/examples/clingo/sudoku>`_.

Client-Server
+++++++++++++

To run `clinguin` one can the execute the following command:

.. code-block:: bash

    $ clinguin client-server --source-files examples/clingo/sudoku/instance.lp examples/clingo/sudoku/encoding.lp --widget-files examples/clingo/sudoku/ui.lp


After execution a Sudoku window should open, where one can play a round of Sudoku. The look of the window will vary depending on the OS.

.. figure:: ../../../../examples/clingo/sudoku/sudoku.png


The `client-server` option provided in the command line, states that both client and server shall be started at the same time, so it has the look and feel of a single program. If one wants to seperate `client` and `server`, one could start them in two shells

Server
++++++
.. code-block:: bash

    $ clinguin server --source-files examples/clingo/sudoku/instance.lp examples/clingo/sudoku/encoding.lp --widget-files examples/clingo/sudoku/ui.lp

The source and gui files are only specified for the server, the client does not need to care about this. As one can see, we have specified three files: ``instance.lp``, ``encoding.lp`` and ``ui.lp``. This is a common separation for `clinguin`, therefore one can at first experiment with the encoding/problem one is working on, and after that create a ui for the problem, to showcase, debug, etc. 

When running the server one can further specify the *Backend* that should be used. See the :ref:`customize_guide` for more information.

Client
++++++

.. code-block:: bash

    $ clinguin client 

The client does not need any files as input since it will ask the server for the information.

When running the client one can further specify the *Frontend* that should be used. See the :ref:`customize_guide` for more information. See the :ref:`customize_guide` for more information.

Basic example
=============

After the startup of your first `clinguin` example, it is now time to understand the basic techniques how to write your own UI encoding. For this you must create two files:

* ``empty.lp`` An empty file which will be used instead of a domain specific encoding.
* ``ui.lp`` A ui-file that will define the look and interactivity of your interface.

To define a UI, `clinguin` uses three different predicates:

* ``element(ID,TYPE,PARENT)``:  Corresponds to an element in the Gui (button, frame, etc).
* ``attribute(ID_OF_ELEMENT,KEY,VALUE)``: used to set various attributes of an element, (background-color, font, etc). 
* ``callback(ID_OF_ELEMENT,ACTION,POLICY)``: Used to define how an element behaves (how = policy) on certain actions.

.. note::
    
    Each `clinguin` ``ui.lp`` file must contain exactly one element of type ``window``. 

.. rubric:: *Example*
    :name: example-window

For example, the following code generates a window with the dimensions 400x400 and with the background color pink:

.. code-block::

    element(window, window, root).
    attribute(window, height, 400).
    attribute(window, width, 400).
    attribute(window, background_color, pink).

The next task is to execute this program and show actually the window. This can be done by:

.. code-block:: bash

    $ clinguin client-server --source-files empty.lp --widget-files ui.lp


Syntax
======

As now one can imagine, `clinguin` features a bunch of pre-defined element types:

* window
* container
* button
* label
* dropdown_menu

    * dropdown_menu_item

* message
* menu_bar

    * menu_bar_section

        * menu_bar_section_item

* canvas

For each of these element types there exists a bunch of available attributes. One can look the up by typing:

.. code-block:: bash
    
    $ clinguin client-server --gui-syntax

If one is  also interested in what values one might set, one can also look at the full syntax:

.. code-block:: bash
    
    $ clinguin client-server --gui-syntax-full


Our next example captures a bit more how one structures the gui. For this we take a simple logic program as our source-file (e.g. `source.lp`), which has two models: `p(1)` and `p(2)`:

.. code-block::

    1{p(1);p(2)}1.


Now we create a Gui (e.g. `ui.lp`), where we assume either `p(1)` or `p(2)` and provide a functionality to reset it:

.. code-block::

    element(window, window, root).
    attribute(window, height, 400).
    attribute(window, width, 400).

    element(dpm, dropdown_menu, window).
    attribute(dpm, selected, V) :- p(V).

    element(dmp(V), dropdown_menu_item, dpm) :- _b(p(V)).
    attribute(dmp(V), label, V) :- _b(p(V)).
    callback(dmp(V), click, add_assumption(p(V))) :- _b(p(V)).

    element(l, label, window).
    attribute(l, label, "Clear assumptions").
    attribute(l, font_weight, "italic").
    attribute(l, font_size, 20).
    attribute(l, background_color, "#ff4d4d").
    attribute(l, on_hover, "True").
    attribute(l, on_hover_background_color, "#990000").
    callback(l, click, clear_assumptions).

With this done, we can start our application:

.. code-block:: bash

    $ clinguin client-server --source-files source.lp --widget-files ui.lp


We have four different elements:

1. window 

    * As in the previous example it just defines the size of the window.

2. dpm (dropdown_menu) 

    * It's parent is the `window` which means, that it is directly shown below the window. 
    * The attribute `selected` can be used to show the text in the ''selected'' field of the dropdown.

3. dpm(V) (dropdown_menu_item) 

    * A dropdown_menu_item can only be the child of a dropdown_menu (and no other element type)
    * We want to have one item for each model, therefore we have the `_b(p(V))` in the body. The enclosing `_b` of a symbol means, that we reason bravely (so basically the union of all models), therefore we have here both `p(1)` and `p(2)`.
    * We add two attributes: One to define the text (attribute key `label`) and what shall happen on a click (then we want to add the assumption, that either `p(1)` or `p(2)` exist).

4. b (label)

    * We use this label to display the text `Clear assumptions` and further create an action, that when one clicks on it, all assumptions are cleared.
    * All other attributes are only there for the look and feel of the label (on hover, etc.)

Available policies:
-------------------

Above we have seen two different policies: `add_assumption` and `clear_assumptions`. Therefore one might wonder what kinds of policies are actually available? - It is pointed out here, that this can currently onle be looked up in the API documentation under the section `Server`/`Server Default Backends`/`ClingoBackend` (class `ClingoBackend`).
















