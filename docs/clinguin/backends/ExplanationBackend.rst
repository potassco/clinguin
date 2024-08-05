ExplanationBackend
------------------

Extends :ref:`ClingoMultishotBackend` with functionality to compute Minumal Unsatisfiable Sets (MUS) when there is an UNSAT output.

.. admonition:: Examples


    * `sudoku_advanced <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku_advanced>`_
    * `sudoku_explained <https://github.com/krr-up/clinguin/tree/master/examples/tkinter/sudoku_explained>`_

When the :ref:`domain-control` produces an unsatisfiable output this backend will perform subsequents calls
to find the subset minimal assumptions that caused the unsatisfiablity.
The :ref:`domain-state` is then enhanced by the MUS using predicate ``_clinguin_mus/1``.

.. admonition:: MUS Basic Example

    For instance in the program ``{a(1..4)}. :-a(1),a(2). :-a(3).`` if it is solved considering ``a(1)`` ``a(3)`` and ``a(4)`` as assumptions,
    it will lead to an unsatisfiable output.
    The MUS will be a subset of these assumptions such that removing any assumption will make the program satisfiable.
    Therefore, ``a(3)`` would be the only member in the MUS since it alone causes the unsatisfiablity with the last constraint.
    As such, the atom ``_clinguin_mus(a(3))``  will be added to the :ref:`domain-state`.


.. admonition:: Example Sudoku


    In the sudoku, the MUS information will show in red the faulty assumptions.

    .. code-block::

        attr(pos(X,Y),class,"bg-primary"):-pos(X,Y), not _clinguin_mus(sudoku(X,Y,_)), not _clinguin_mus(initial(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(sudoku(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(initial(X,Y,_)).

**Including instance facts in the MUS**


This is needed when some of the input facts also want to be shown to the user.
The ExplanationBackend adds an argument to the command line: ``--assumption-signature``
in which the user can select which signatures will be considered as assumptions in the MUS computation.
To achive this behaviour, the domain files will be internally transformed,
so that all facts for atoms matching the signatures provided in this arguments are considered choices and automatically added as true assumptions.

.. currentmodule:: clinguin.server.application.backends


.. admonition:: Examples


    The `sudoku_advanced <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku_advanced>`_ example
    provides the argument ``--assumption-signature=initial,3``. By doing so, all the initial values in the instance
    of the sudoku are transfored into choices and enforced by considering them as assumptions.
    This way, they are also considered in unsatisfiable set and shown to the user.

Public operations
+++++++++++++++++

Can be used as `OPERATION` in the actions of the :ref:`ui-state`.
Also includes all public operations from the :ref:`ClingoMultishotBackend`.

.. autoclass:: ExplanationBackend
    :members:
    :noindex:
    :exclude-members: register_options


Domain state constructors
+++++++++++++++++++++++++

.. important::

    The domain state also inclues domain constructors from the :ref:`ClingoMultishotBackend`

.. autoproperty:: ExplanationBackend._ds_mus

