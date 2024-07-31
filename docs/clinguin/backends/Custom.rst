Creating your own backend
-------------------------

By creating your own backend you can extend functionality and edit the existing server workflow.
If you are using clingo, we highly recomend extending the  :ref:`ClingoMultishotBackend` to create your own.
This backend contains multiple functionalities already built in wich can be overwritten and extended.
The following explanation assumes that this is the backend that is being extended.

.. note::

    If you will not use multi-shot functionalities, assumptions and exterals
    you can also extend the :ref:`ClingoBackend`.

.. note:: **Using your backend**

    To make your custom backend avaliable to clinguin, you must provide the path via the command line argument ``--custom-classes``.

In what follows we divide the possible extensions. For more implementation details, look at the
`source code <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingo_multishot_backend>`_
All the presented methods can be overwritten to your desire.


Constructor
++++++++++++

In the constructor one can add custom arguments and new domain-state constructors.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_

.. currentmodule:: clinguin.server.application.backends

.. automethod:: ClingoMultishotBackend.__init__


Register options
++++++++++++++++

By overwritting this class method, one can add new arguments to the command line.
These options will be added under a group for the created backend.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_

.. automethod:: ClingoMultishotBackend.register_options

Setups
++++++

These methods will handle the arguments depending on the clinguin state.
Some are called at the start after a restart or when a change is done in the solving.
When a custom argument is added to the backend if will likely need to be handled here.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_


.. automethod:: ClingoMultishotBackend._restart

.. automethod:: ClingoMultishotBackend._init_ds_constructors

.. automethod:: ClingoMultishotBackend._init_command_line

.. automethod:: ClingoMultishotBackend._init_interactive

.. automethod:: ClingoMultishotBackend._init_ctl

.. automethod:: ClingoMultishotBackend._create_ctl

.. automethod:: ClingoMultishotBackend._load_and_add

.. automethod:: ClingoMultishotBackend._load_file

.. automethod:: ClingoMultishotBackend._outdate

.. automethod:: ClingoMultishotBackend._is_browsing


Solving
+++++++

These methods are involved on how the domain control is solved.
They can be ovweritten for theory extensions among other things.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_

.. automethod:: ClingoMultishotBackend._ground

.. automethod:: ClingoMultishotBackend._prepare

.. automethod:: ClingoMultishotBackend._on_model

.. automethod:: ClingoMultishotBackend._add_atom


UI updates
++++++++++

If any changes want to be made in how the UI state is computed they
can be made by overwritting this method.

.. admonition:: Examples


    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_


.. automethod:: ClingoMultishotBackend._update_ui_state


Domain state
++++++++++++

These methods take care of generating the :ref:`domain-state`.
When new information wants to be added a domain state constructor can be included.
These domain constructors will be automatically called by the `_domain_state` property.
But, they need to be previously registered in the constructor using the functions below.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
    * `clingodl_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingodl_backend.py>`_
    * `clingraph_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/clingraph_backend.py>`_

.. note::

    Some of the domain constructors involve extra work so they are handled as ``@cache_property``.

.. warning::

    Make sure any domain constructor added is a property with anotation ``@property``

.. automethod:: ClingoMultishotBackend._add_domain_state_constructor

.. automethod:: ClingoMultishotBackend._clear_cache

.. note::

    Domain state constructors for this backend are showed in the section above.
    These constructors can also be overwritten if necessary.


Public operations
+++++++++++++++++

Each backend can define any number public operations or overwrite the existing ones.
These operations are any public method of the class and will be accessible to the UI.

.. admonition:: Examples


    * `explanation_backend <https://github.com/krr-up/clinguin/tree/master/clinguin/server/application/backends/explanation_backend.py>`_
