Frontends
#########

The frontends listed here are provided with clinguin. Each frontend allows different element types, arguments, and events.

The source code for the frontends can be found on `GitHub <https://github.com/krr-up/clinguin/tree/master/clinguin/client/presentation/frontends>`_.

AbstractFrontend
----------------

Serves as the most basic class for creating a custom frontend.

.. currentmodule:: clinguin.client.presentation.abstract_frontend

.. autoclass:: AbstractFrontend

TkinterFrontend
---------------

This frontend extends the :ref:`AbstractFrontend` using the standard Python interface `tkinter <https://docs.python.org/3/library/tkinter.html>`_ to generate a UI.

.. admonition:: Examples
    :class: example

    * `Tkinter Example <https://github.com/krr-up/clinguin/tree/master/examples/tkinter>`_

One can look up the available elements, with the corresponding attributes and callback actions using:

.. code-block:: bash

    $ clinguin client-server --frontend-syntax

If one is also interested in what values one might set, one can also look at the full syntax:

.. code-block:: bash

    $ clinguin client-server --frontend-syntax-full

AngularFrontend
---------------

This frontend was developed using `Angular <https://angular.io/guide/setup-local>`_.
For styling, it uses the `bootstrap <https://getbootstrap.com/>`_ library with `Angular-Boostrap <https://ng-bootstrap.github.io/#/home>`_.
Thus, providing beautiful components out of the box by giving access to Bootstrap classes for styling.
For contributing with new components take a look at eth :ref:`Development` section.

.. admonition:: Examples
    :class: example

    * `Angular Example <https://github.com/krr-up/clinguin/tree/master/examples/angular>`_

.. tip::

    It is encouraged to style the UI using the `bootstrap classes <https://getbootstrap.com/docs/4.0/utilities/borders/>`_. This can be done in any element using the attribute ``class``, which can appear multiple times.


Elements
++++++++

It implements most of the elements and attributes of tkinter.


``window``
.........

``menu-bar``
............

``message``
............

``context-menu``
................

``modal``
.........

``container``
.............

``button``
..........

``label``
.........

``textfield``
.............

``dropdown-menu``
.................

``dropdown-menu-item``
......................

``canvas``
...........

Creating Your Own Frontend
--------------------------

.. warning::
    Under construction. Sorry :)
