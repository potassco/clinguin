
Backends
########

The backends listed here are provided with clinguin. 
All available functions for each backend are listed below.

The source code for the backends can be found  in `github <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends>`_.

ClinguinBackend
---------------

    Serves as the must basic class for creating a custom backend.
    This class does not have any clingo functionalities.

    .. currentmodule:: clinguin.server.application.clinguin_backend

    .. autoclass:: ClinguinBackend
        :members:


.. currentmodule:: clinguin.server.application.backends

ClingoBackend
---------------

    Exteds :ref:`ClinguinBackend` with basic clingo functionality for single-shot solving.

    .. admonition:: Examples
        :class: example

        * `sudoku_single_shot <https://github.com/krr-up/clinguin/tree/master/examples/tkinter/sudoku_basic>`_



    .. autoclass:: ClingoBackend
        :members:


ClingoMultishotBackend
----------------------

    Extends :ref:`ClingoBackend` with functionality for multi-shot solving. Adds options to access and store assumptions and externals.

    .. admonition:: Examples
        :class: example

        * `sudoku <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku>`_
        * `jobshop <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop>`_
        * `placement <https://github.com/krr-up/clinguin/tree/master/examples/angular/placement>`_


    .. autoclass:: ClingoMultishotBackend
        :members:


ClingraphBackend
----------------

    Extends :ref:`ClingoMultishotBackend` with functionality to render and interact with `clingraph <https://clingraph.readthedocs.io/en/latest/>`_ images.

    .. admonition:: Examples
        :class: example

        * `graph_coloring <https://github.com/krr-up/clinguin/tree/master/examples/angular/graph_coloring>`_
        * `tree_browser <https://github.com/krr-up/clinguin/tree/master/examples/angular/tree_browser>`_
        * `ast <https://github.com/krr-up/clinguin/tree/master/examples/angular/ast>`_


    .. autoclass:: ClingraphBackend
        :members:


ExplanationBackend
------------------

    .. admonition:: Examples
        :class: example

        * `sudoku_advanced <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku_advanced>`_


    .. autoclass:: ExplanationBackend
        :members:


Creating your own backend
-------------------------


    .. autofunction:: clinguin.server.application.backends.ClingoBackend._init_setup