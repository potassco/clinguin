
Communication
#############

****
GET
****
.. figure:: ../../get.png

When the UI is first loaded and in every reload, the client will do a ``GET`` request which will update the UI.

****
POST
****

.. figure:: ../../post.png

When the user triggers as event that is associiated with a ``call`` action, the client will do a ``POST`` request.
This request will include the selected operations and the context.


**********
Operations
**********

.. figure:: ../../operation.png

The operations are defined by the backend. These operations will interact with the domain control while performing all the required changes. 
Each backend will define an available list of operations. These lists can be found in :ref:`Backends`.


********
Context
********

.. figure:: ../../context.png


The context can be used to store information provided by the user before calling the server. For instance, it can store the input of a text field, or the value of a checkbox. Therefore, it is usefull for creating input forms within the UI. Internally, the context is represented by a dictionary in the client and it can be accesed in three ways.

.. warning::
Context information is only available for web frontends and not for Tkinter.


**Updates**

The context information is updated using predicate ``when`` as described above. 

.. admonition:: Example
    :class: example

    The context would be updated with the key-value pair `(agree, true)` when `button1` is clicked.

    .. code-block:: 

        when(button1, click, context, (agree, true)).

To use a value imputed by the user, such as for text fields, the special constant ``_value`` will hold the value of an input event. 

.. admonition:: Example
    :class: example

    .. code-block:: 
        
        when(textfield1, input, context, (t1_content, _value)).


**Substitution**

The values of the context can be accessed for a direct substitution in the operation of a call. This is done with the special predicates ``_context_value/1`` and ``_context_value_optional/1``. The argument of these predicates is the key which will be substituted by the value before it is processed by the server. While ``_context_value/1`` will show an error in case there is no value for the provided key, ``_context_value_optional/1`` will leave the input optional, and in case there is no value present it is substitued by None.

.. admonition:: Example
    :class: example

    Example from  the `ast example <https://github.com/krr-up/clinguin/tree/master/examples/angular/ast/ui.lp>`_.
    The key `selected_node` is set open clicking on a node and then this information is sustituted on the next line when the server is called to add an atom, which yeilds operation ``add_atom(show_children(X,true)))`` after the substitution, with ``X`` being the selected node.

    .. code-block:: 

        when(node(X), click, context, (selected_node, X)):- node(X).
        when(button1, click, call, add_atom(show_children(_context_value(selected_node),true))).

**Access**

All calls to the server will include the context as an argument. All backends will have access to this dictionary and can use its values for any operation. The provadided backends include the context information as part of the :ref:`domain-state` via predicate ``_clinguin_context(KEY,VALUE)``. Thus, giving the UI encoding access to the context at the time the call was made. Beware that changes in the context are not reflected in the UI encoding imidiatley, but only after calling the server and calculating the UI again. 


.. warning::
    The context is erased after every call to the server.


.. tip::
    If some of the context wants to be preserved between calls to the server, it can be done manually in the UI encoding by using the event ``load`` of the ``window``. An example is provided below, which is used in the `ast example <https://github.com/krr-up/clinguin/tree/master/examples/angular/ast/ui.lp>`_.

    .. code-block:: 
    
        when(window, load, context, (selected_node, X)):- _clinguin_context(selected_node, X).




********
JSON UI
********

.. figure:: ../../json.png


The :ref:`ui-state` is represented by a JSON to comunicate between client and server. This JSON is generated in a herachical fashion where each element apears with the following form. 

.. code-block::

    {
        "id": <the id of the element>,
        "type": <the type of the element>,
        "parent": <the id of the partent element>,
        "attributes": <the list of associated attribute> 
            [
                {
                    "id": <the id of the element>,
                    "key": <attribute key>,
                    "value": <attribute value>
                },
                ...
            ],
        "when": <the list of associated actions> 
            [
                {
                    "id": <the id of the element>,
                    "event": <the event>,
                    "interaction_type": <the interaction type>,
                    "policy": <the operation>
                }
            ],
        "children": <the list of all children>[]
    }


.. admonition:: Example
    :class: example

    The following :ref:`ui-state` the corresponding JSON UI can be found below.


    .. code-block::

        elem(w, window, root).
        elem(b1, button, w).
        attr(b1, label, "Button 1").
        when(b1, click, call, next_solution).


    .. code-block::

        {
            "id":"root",
            "type":"root",
            "parent":"root",
            "attributes":[],
            "when":[],
            "children":[
                {
                    "id":"w",
                    "type":"window",
                    "parent":"root",
                    "attributes":[],
                    "when":[],
                    "children":[
                        {
                        "id":"b1",
                        "type":"button",
                        "parent":"w",
                        "attributes":[
                            {
                                "id":"b1",
                                "key":"label",
                                "value":"\"Button 1\""
                            }
                        ],
                        "when":[
                            {
                                "id":"b1",
                                "event":"click",
                                "interaction_type":"call",
                                "policy":"next_solution"
                            }
                        ],
                        "children":[]
                        }
                    ]
                }
            ]
        }







