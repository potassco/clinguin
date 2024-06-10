ExplanationBackend
------------------

Extends :ref:`ClingoMultishotBackend` with functionality to compute Minumal Unsatisfiable Cores (MUC) when there is an UNSAT output.

.. admonition:: Examples


    * `sudoku_advanced <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku_advanced>`_
    * `sudoku_explained <https://github.com/krr-up/clinguin/tree/master/examples/tkinter/sudoku_explained>`_


When the :ref:`domain-control` produces an unsatisfiable output this backend will perform subsequents calls
to find the subset minimal assumptions that caused the unsatisfiablity.
These assuptions not only include those selected by the user, but also can be part of the input.
This is needed when some of the input facts also want to be shown to the user.
Therefore, this backend adds an argument to the command line: ``--assumption-signature``
in which the user can select which signatures will be considered as assumptions in the MUC computation.

.. currentmodule:: clinguin.server.application.backends


.. admonition:: Examples


    The `sudoku_advanced <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku_advanced>`_ example
    provides the argument ``--assumption-signature=initial,3`` so that all the initial values of the sudoku
    are also considered in the unsat core and therefore shown to the user.

    .. code-block::

        attr(pos(X,Y),class,"bg-primary"):-pos(X,Y), not _clinguin_mus(sudoku(X,Y,_)), not _clinguin_mus(initial(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(sudoku(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(initial(X,Y,_)).

The :ref:`domain-state` is then enhanced by the MUC using predicate ``muc/1``.

.. admonition:: Examples


    In the sudoku, the MUC information will show in red the faulty assumptions.

    .. code-block::

        attr(pos(X,Y),class,"bg-primary"):-pos(X,Y), not _clinguin_mus(sudoku(X,Y,_)), not _clinguin_mus(initial(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(sudoku(X,Y,_)).
        attr(pos(X,Y),class,"bg-danger"):-pos(X,Y), _clinguin_mus(initial(X,Y,_)).


.. autoclass:: ExplanationBackend
    :members:
    :noindex:
    :exclude-members: register_options


Domain state constructors

The domain state also inclues domain constructors from the parent class.

.. automethod:: ExplanationBackend._ds_mus