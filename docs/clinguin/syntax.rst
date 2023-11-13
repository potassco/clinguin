
Syntax and Components
#####################

One can look the up the available elements, with the corresponding attributes and callback actions using:

.. code-block:: bash

    $ clinguin client-server --frontend-syntax

If one is  also interested in what values one might set, one can also look at the full syntax:

.. code-block:: bash

    $ clinguin client-server --frontend-syntax-full


``element(ID,TYPE,PARENT)``
+++++++++++++++++++++++++++

* ``ID`` Identifies the element for further references.

* ``TYPE`` The type of element (``window``, ``container``, ``button`` etc)

* ``PARENT`` The id of the parent element. The ``root`` identifier is used as the root element of the UI.

``attribute(ID_OF_ELEMENT,KEY,VALUE)``
++++++++++++++++++++++++++++++++++++++

For each of these element types there exists a bunch of available attributes to set how the element will look like.

* ``ID_OF_ELEMENT`` Identifier of the element setting the attribute to

* ``KEY`` The name of the attribute

* ``Value`` The value of the attribute


``callback(ID_OF_ELEMENT,ACTION,POLICY)``
+++++++++++++++++++++++++++++++++++++++++

* ``ID_OF_ELEMENT`` Identifier of the element to which the action is performed

* ``ACTION`` The action performed (``click``, ``hover``, etc). Each element allows different actions.

* ``POLICY`` The functionality from the Backend that will be called when the action is performed on the element. The available policies can be looked up in the API documentation under the section `Server`/`Server Backends`/`ClingoMultishotBackend` (class `ClingoMultishotBackend`).


Elaborated example
++++++++++++++++++


This example captures a bit more how one structures the frontend. For this we take a simple logic program as our domain-file (e.g. `domain.lp`), which has two models: `p(1)` and `p(2)`:

.. code-block::

    1{p(1);p(2)}1.


Now we create a UI (e.g. ``ui.lp``), where we assume either ``p(1)`` or ``p(2)`` and provide a functionality to reset it:

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

    $ clinguin client-server --domain-files domain.lp --ui-files ui.lp

.. figure:: ../basic-ui.png


We have four different elements:

1. ``window`` (window)

    * As in the previous example it just defines the size of the window.

2. ``dpm`` (dropdown_menu)

    * It's parent is the ``window`` which means, that it is directly shown below the window.
    * The attribute ``selected`` can be used to show the text in the ''selected'' field of the dropdown.

3. ``dpm(V)`` (dropdown_menu_item)

    * A dropdown_menu_item can only be the child of a dropdown_menu (and no other element type)
    * We want to have one item for each model, therefore we have the ``_b(p(V))`` in the body. The atom preceded by an underscore: ``_b`` means, that we reason bravely (so basically the union of all models), therefore we have here both ``p(1)`` and ``p(2)``.
    * We add an attribute to define the text (attribute key ``label``)
    * We add a callback to define what shall happen on a click. In this case the policy ``add_assumption`` is called with the parameter ``p(V)``. Doing so, we add the assumption, that either ``p(1)`` or ``p(2)`` exist.

4. ``l`` (label)

    * We use this label to display the text `Clear assumptions` and further create an action, that when one clicks on it, all assumptions are cleared.
    * All other attributes are only there for the look and feel of the label (on hover, etc.)













