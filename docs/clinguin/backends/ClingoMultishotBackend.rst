
ClingoMultishotBackend
----------------------

Extends :ref:`ClingoBackend` with functionality for multi-shot solving. Adds options to access and store assumptions and externals.

.. admonition:: Examples
    

    * `sudoku <https://github.com/krr-up/clinguin/tree/master/examples/angular/sudoku>`_
    * `jobshop <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop>`_
    * `placement <https://github.com/krr-up/clinguin/tree/master/examples/angular/placement>`_

.. currentmodule:: clinguin.server.application.backends

.. autoclass:: ClingoMultishotBackend
    :members:
    :noindex:
    :exclude-members: register_options

**Domain state constructors**  

The domain state also inclues domain constructors from the parent class.

.. automethod:: ClingoMultishotBackend._ds_assume