FclingoBackend
---------------

Extends :ref:`ClingoBackend` with functionality to accept `fclingo <https://github.com/potassco/fclingo/tree/master>`_ programs as input.


.. admonition:: Examples


    * `tax <https://github.com/krr-up/clinguin/tree/master/examples/angular/tax>`_


The :ref:`domain-state` is then enhanced by predicate ``_clinguin_assign/2``.
See `ClingoDLBackend <./ClingoDLBackend.rst>`_ for details.

.. warning::

    Notice that assignments are not part of the brave or cautious consequences

.. tip::

    To know if the value of a variable is defined in the current model, check the appearance of predicate ``__def/1`` as part of the model.

.. currentmodule:: clinguin.server.application.backends

Public operations
+++++++++++++++++

Can be used as `OPERATION` in the actions of the :ref:`ui-state`.

Also includes all public operations from the :ref:`ClingoBackend`.

.. autoclass:: FclingoBackend
    :members:
    :noindex:
    :exclude-members: register_options


Domain state constructors
+++++++++++++++++++++++++

.. important::

    The domain state also includes domain constructors from the :ref:`ClingoBackend`

.. autoproperty:: FclingoBackend._ds_assign
