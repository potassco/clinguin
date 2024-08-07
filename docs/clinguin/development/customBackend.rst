.. _CustomBackend:

Creating your own backend
-------------------------

By creating your own backend you can extend functionality and edit the existing server workflow.
If you are using *clingo*, we highly recomend extending the  :ref:`ClingoBackend` to create your own.
This backend contains multiple functionalities already built in wich can be overwritten and extended.
The following explanation assumes that this is the backend that is being extended.


Code structure
==============

Your code strucure with your custom backend must be the following:

.. code-block::

    my_project/
    ├── my_backend.py
    └── ui.lp
    └── encoding.lp
    └── instance.lp

- ``my_backend.py``: Contains the backend class that extends the :ref:`ClingoBackend`.

.. code-block:: python

    from clinguin.server.application.backends import ClingoBackend

    class MyBackend(ClingoBackend):
        ...

- ``ui.lp``: Contains the UI encoding.
- ``encoding.lp``: Contains the domain encoding.
- ``instance.lp``: Contains the instance.

Using this structure the command line, standing insde folder `my_project` would be the following:

.. code-block:: console

    $ clinguin client-server --domain-files instance.lp encoding.lp --ui-files ui.lp --custom-classes my_backend.py --backend MyBackend

.. tip::

    You can make sure your backend class is avaliable by checking the help using ``-h`` with your custom classes:

    .. code-block:: console

        $ clinguin client-server --domain-files instance.lp encoding.lp --ui-files ui.lp --custom-classes my_backend.py -h


.. note:: **Using your backend**

    To make your custom backend avaliable to clinguin, you must provide the path via the command line argument ``--custom-classes``.


Customizations
==============

In what follows we divide the possible extensions for explanability. For more implementation details, look at the source code

.. currentmodule:: clinguin.server.application.backends

.. autoclass:: ClingoBackend
    :exclude-members: __init__, __new__

.. autoclass:: ClingoBackend
    :exclude-members: __init__, __new__
    :show-inheritance:

Register options
++++++++++++++++

By overwritting this class method, one can add new arguments to the command line.
These options will be added under a group for the created backend. The value can be set in :meth:`~ClingoBackend._init_command_line`.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_


.. automethod:: ClingoBackend.register_options

Public operations
+++++++++++++++++

Each backend can define any number public operations or overwrite the existing ones.
These operations are any public method of the class and will be accessible to the UI.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_



.. admonition:: Example


    This example shows how to add a a new public operation in a backend

    .. code-block::

        class MyBackend(ClingoBackend):
            ...

            def my_operation(self, arg1, arg2)->None:
                # Do something using the given arguments
                # Does not return anything

    Use it in your :ref:`ui-files` like this:

    .. code-block::

        when(button1, click, call, my_operation("arg1", "arg2")).

.. warning::

    - If the operation made impacts the current broswsing state make sure to call the :meth:`~ClingoBackend._outdate` method.
    - If the operation make the current control outdated (for instnce adds an atom or a program), make sure to call the :meth:`~ClingoBackend._init_ctl` method.


Initialization
++++++++++++++

These methods will handle the arguments depending on the current state of the interaction.
Some are called at the start after a restart or when a change is done in the solving.


.. admonition:: Examples

    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_
    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_


.. automethod:: ClingoBackend._restart

.. automethod:: ClingoBackend._init_ds_constructors

.. automethod:: ClingoBackend._init_command_line

.. automethod:: ClingoBackend._init_interactive

.. automethod:: ClingoBackend._init_ctl

.. automethod:: ClingoBackend._create_ctl

.. automethod:: ClingoBackend._load_and_add

.. automethod:: ClingoBackend._load_file

.. automethod:: ClingoBackend._outdate


Solving
+++++++

These methods are involved on how the domain control is solved.
They can be ovweritten for things such as theory extensions.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_

.. automethod:: ClingoBackend._ground

.. automethod:: ClingoBackend._prepare

.. automethod:: ClingoBackend._on_model



Setters
+++++++

These methods will set different attributes of the backend.

.. automethod:: ClingoBackend._add_domain_state_constructor

.. automethod:: ClingoBackend._set_context

.. automethod:: ClingoBackend._set_constant

.. automethod:: ClingoBackend._add_atom

.. automethod:: ClingoBackend._set_external

.. automethod:: ClingoBackend._add_assumption



Domain state
++++++++++++

The domain state constructors take care of generating the :ref:`domain-state`.
When new information wants to be added a domain state constructor can be included.
These domain constructors will be automatically called by the `_domain_state` property.
But, they need to be previously registered in the constructor using the functions below.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_

.. admonition:: Example


    This example shows how to add a custom domain constructor

    .. code-block::

        @property
        def _ds_my_custom_constructor(self):
            # Creates custom program
            return "my_custom_program."

        def _init_ds_constructors(self):
            super()._init_ds_constructors()
            self._add_domain_state_constructor("_ds_my_custom_constructor")


.. warning::

    Make sure any domain constructor added is a property with anotation ``@property`` or ``@cache_property`` if the computation is costly.

.. warning::

    Some domain constructors will be skiped if they are not used in the ui-files.
    This can be done in a custom method domain_constructor using the following code:

    .. code-block::

        @cache_property
        def _ds_my_custom_complex_constructor(self):
            # Creates custom program
            if not self._ui_uses_predicate("_my_ds_predicate", 1):
                return "% NOT USED\n"
            return "my_custom_program."




.. note::

    Domain state constructors for this backend are showed in the :ref:`ClingoBackend` and :ref:`ClingoBackend` sections.
    These constructors can also be overwritten if necessary.


UI updates
++++++++++

If any changes want to be made in how the UI state is computed they
can be made by overwritting this method.

.. admonition:: Examples


    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_


.. automethod:: ClingoBackend._update_ui_state

.. currentmodule:: clinguin.server.data.ui_state

.. autoclass:: UIState
    :exclude-members: __init__, __new__
