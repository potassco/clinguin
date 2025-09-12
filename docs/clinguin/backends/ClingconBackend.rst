ClingconBackend
---------------

Extends :ref:`ClingoBackend` with functionality to accept `clingcon <https://potassco.org/clingcon/>`_ programs as input.


The :ref:`domain-state` is then enhanced by predicate ``_clinguin_assign/2``.
See `ClingoDLBackend <./ClingoDLBackend.rst>`_ for details.

.. warning::

    Notice that assignments are not part of the brave or cautious consequences

.. currentmodule:: clinguin.server.application.backends

Public operations
+++++++++++++++++

Can be used as `OPERATION` in the actions of the :ref:`ui-state`
Also includes all public operations from the :ref:`ClingoBackend`.

.. autoclass:: ClingconBackend
    :members:
    :noindex:
    :exclude-members: register_options


Domain state constructors
+++++++++++++++++++++++++

.. important::

    The domain state also includes domain constructors from the :ref:`ClingoBackend`

.. autoproperty:: ClingconBackend._ds_assign
