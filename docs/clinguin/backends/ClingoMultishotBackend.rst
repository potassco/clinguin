
ClingoMultishotBackend
----------------------

Extends :ref:`ClingoBackend` with functionality for multi-shot solving. Adds options to access and store assumptions and externals.

.. admonition:: Examples


    * `sudoku <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku>`_
    * `jobshop <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop>`_
    * `placement <https://github.com/krr-up/clinguin/tree/master/examples/angular/placement>`_
    * `placement_optimized <https://github.com/krr-up/clinguin/tree/master/examples/angular/placement_optimized>`_

.. currentmodule:: clinguin.server.application.backends

Public operations
+++++++++++++++++

Can be used as `OPERATION` in the actions of the :ref:`ui-state`
Also includes all public operations from the :ref:`ClingoBackend`.

.. autoclass:: ClingoMultishotBackend
    :members:
    :noindex:
    :exclude-members: register_options


Domain state constructors
+++++++++++++++++++++++++

.. important::

    The domain state also inclues domain constructors from the :ref:`ClingoBackend`

.. autoproperty:: ClingoMultishotBackend._ds_assume