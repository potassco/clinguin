ClingoDLBackend
---------------

Extends :ref:`ClingoMultishotBackend` with functionality to accept clingo-dl programs as input.

.. admonition:: Examples
    :class: example

    * `jobshop <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop>`_


The :ref:`domain-state` is then enhanced by predicate ``_clinguin_assign/2``.


.. admonition:: Examples
    :class: example

    In the jobshop example, the assignment is used for the label of the job.

    .. code-block:: 

        elem(tctime(T,ST), label, tc(T,ST)):- _clinguin_assign((T,ST),Start).
        attr(tctime(T,ST), label, @concat("","@",Start,"-",Start+ET)):- _clinguin_assign((T,ST),Start), executionTime(T,ST,ET).
        attr(tctime(T,ST), class, "fw-light"):- _clinguin_assign((T,ST),Start).
        attr(tctime(T,ST), fontSize, "8px"):- _clinguin_assign((T,ST),Start).

.. warning::

    Notice that asisgnments are not part of the brave or cautious consequences

.. currentmodule:: clinguin.server.application.backends

.. autoclass:: ClingoDLBackend
    :members:
    :noindex:
    :exclude-members: register_options


**Domain state constructors**  

The domain state also inclues domain constructors from the parent class.

.. automethod:: ClingoDLBackend._ds_assign
