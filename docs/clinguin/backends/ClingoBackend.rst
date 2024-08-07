ClingoBackend
---------------

Implements all basic `clingo's API <https://potassco.org/clingo/python-api/current/clingo/>`_ functionality.
This includes grounding, solving, cautious and brave resoning, use of extenrals and assuptions, and optimization

.. admonition:: Examples

    * `sudoku <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku>`_
    * `jobshop <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop>`_
    * `placement <https://github.com/krr-up/clinguin/tree/master/examples/angular/placement>`_


.. currentmodule:: clinguin.server.application.backends


Public operations
+++++++++++++++++

Can be used as `OPERATION` in the actions of the :ref:`ui-state`

.. autoclass:: ClingoBackend
    :members:
    :noindex:
    :exclude-members: register_options, get, __init__


Domain state constructors
+++++++++++++++++++++++++


.. autoproperty:: ClingoBackend._ds_context

.. autoproperty:: ClingoBackend._ds_model

.. autoproperty:: ClingoBackend._ds_brave

.. autoproperty:: ClingoBackend._ds_cautious

.. autoproperty:: ClingoBackend._ds_brave_optimal

.. autoproperty:: ClingoBackend._ds_cautious_optimal

.. autoproperty:: ClingoBackend._ds_assume

.. autoproperty:: ClingoBackend._ds_external

.. autoproperty:: ClingoBackend._ds_opt

.. autoproperty:: ClingoBackend._ds_unsat

.. autoproperty:: ClingoBackend._ds_browsing

.. autoproperty:: ClingoBackend._ds_constants