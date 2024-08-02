ClingoBackend
---------------

Implements all basic clingo functionality for single-shot solving.

.. admonition:: Examples
    :class: example

    * `sudoku_single_shot <https://github.com/krr-up/clinguin/tree/master/examples/tkinter/sudoku_basic>`_

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

.. autoproperty:: ClingoBackend._ds_opt

.. autoproperty:: ClingoBackend._ds_unsat

.. autoproperty:: ClingoBackend._ds_browsing

.. autoproperty:: ClingoBackend._ds_constants