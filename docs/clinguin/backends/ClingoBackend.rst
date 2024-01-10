ClingoBackend
---------------

Implements all basic clingo functionality for single-shot solving.

.. admonition:: Examples
    :class: example

    * `sudoku_single_shot <https://github.com/krr-up/clinguin/tree/master/examples/tkinter/sudoku_basic>`_

.. currentmodule:: clinguin.server.application.backends


.. autoclass:: ClingoBackend
    :members:
    :noindex:
    :exclude-members: register_options, get

Domain state constructors
+++++++++++++++++++++++++  

The domain state also inclues domain constructors from the parent class.

.. automethod:: ClingoBackend._ds_context

.. automethod:: ClingoBackend._ds_brave

.. automethod:: ClingoBackend._ds_cautious

.. automethod:: ClingoBackend._ds_model

.. automethod:: ClingoBackend._ds_unsat

.. automethod:: ClingoBackend._ds_browsing