A User Interface is defined in `clinguin` using the three predicates below.

.. note::
    The available element types, attributes, events and actions will vary depending on the frontend. See the details for each front end in the :ref:`Frontends` section.


``elem(ID, TYPE, PARENT)``
+++++++++++++++++++++++++++

    Elements define building blocks of the UI.

    * ``ID`` Identifies the element for further references.

    * ``TYPE`` The type of element (``window``, ``container``, ``button`` etc).

    * ``PARENT`` The id of the parent element. The identifier ``root`` is used as the root element of the UI.


``attr(ID, KEY, VALUE)``
++++++++++++++++++++++++

    Attributes define the style of the UI.

    * ``ID`` Identifier of the element that the attribute will be set to.

    * ``KEY`` The name of the attribute. Avaliable attributes depend on the element type and the frontend.

    * ``VALUE`` The value of the attribute.


``when(ID, EVENT, ACTION, OEPRATION)``
+++++++++++++++++++++++++++++++++++++++++

    Actions define the interactivite of the UI.  Multiple actions are allowed as explaned in :ref:`Multiple actions`. To better understand the execution of actions, we refer the reader to the diagram in the :ref:`Basic Usage`.

    * ``ID`` Identifier of the element that the user interacted with.

    * ``EVENT`` The event that is being triggered, such as ``click``, ``hover``,  ``input``, etc. Each element type allows different events.

    * ``ACTION`` The action performed.  

        * ``call`` Calls the server to perform an operation. 
        * ``update`` Updates the attribute of another element without any calls to the server.
        * ``context`` Updates the internal context that will be passed to the server on the following call actions. See :ref:`Context` for more details.

    * ``OPERATION`` The operation acounts to the information that the action requires for its execution.

        * ``ACTION`` = ``call`` The operation corresponds to an function available in the Backend. The function call is represented as a predicate, for instance ``add_assumption(a)`` or ``next_solution``.
        * ``ACTION`` = ``update`` The operation will be a tuple of size three ``(ID', KEY, VALUE)`` where ``ID'`` is the identifier of the element whose value for attribute ``KEY`` will be updated to ``VALUE``. Notice that ``ID'`` might be different than ``ID``.
        * ``ACTION`` = ``context`` The operation will be a tuple ``(KEY, VALUE)``, which will update the key ``KEY`` in the context dictionary to ``VALUE``. See the :ref:`Context` section for detail information on how to use the context.

    **Multiple actions**

        If multiple occurences of predicate ``when`` are present for the same element and event. All of them will be executed. First, the updates will be performed, followed by context changes and finally server calls. Within each type of action no order can be asured. 

        In the case of multiple apearences of ``call``,  a single call will be placed to the server with the information to execute all actions in any order. For instance, in the example below, when ``button1`` is clicked, the server will recive the instruction to exectute two operations: adding assumption ``a`` and adding assumption ``b`` in any order. For a more evolved example of this feature see the `jobshop example <https://github.com/krr-up/clinguin/tree/master/examples/angular/jobshop/ui.lp>`_

        .. code-block:: 

            when(button1, click, call, add_assumption(a)).
            when(button1, click, call, add_assumption(b)).


        To impose an order, the operation provided must be a tuple, in which case the order of execution is defined by the tuple. For instance, the example below will make sure that assumption ``a`` is added before computing a solution.

        .. code-block:: 

            when(button1, click, call, (add_assumption(a), next_solution)).