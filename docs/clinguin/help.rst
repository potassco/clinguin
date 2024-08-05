
.. _help:

|:speech_balloon:| Help
========================

.. admonition:: **Logging**
    :class: tip

    The first thing to try when things are not working as expected is to turn on the logs and inspect the console.
    The log level can be set to ``DEBUG`` in the command line by adding the flag ``--server-log-level DEBUG``.
    This logs will show the communication between the client and the server, as well as every call that is made to the clingo API internally.
    Information regarding the :ref:`domain-control` will be logged in magenta and regarding the :ref:`ui-control` will be logged in cyan.

    This logs will show the atoms that are part of the :ref:`domain-state` which are passed to your UI encoding.

.. admonition:: **Unexpected atoms in brave/cautious consequences**
    :class: tip

    If you inspect the logs, and the :ref:`domain-state` does not have the expected atoms in your brave ``_any`` or cautious ``_all`` consequences,
    make sure your :ref:`domain-files` don't have any ``#show`` statements.

    The show statements in your :ref:`domain-files` will impact the atoms present in the :ref:`domain-state`.
    If you are using show statements, and you want to use ``_any(a)`` for an atom ``a``, that is not part of your show statements,
    then you have to add ``#project a.`` to your :ref:`domain-files` to get the desired output.
    Furthermore any show statements that output a tuple (function without name) will lead to syntactic issues so thet should be removed.

.. admonition:: **Long response time**
    :class: tip

    If the server is taking too long to respond, first check the logs to make sure the server has not crashed and it is still processing the request.
    With the ``DEBUG`` log level you can see the last call that was made to the clingo API.


    *Brave or cautious consequences*
        If the call is the one to compute the brave or cautious consequences, then the problem might be that your encoding has a very large serach space.
        If you can, avoid using ``all`` or ``any`` in your ui encoding, do so. This way these calls will be skipped (similarly for ``all_opt`` and ``any_opt``).

    *Optimizing*
        If the problem is finding an optimal model you can pass a timeout to the server in the command line with the flag ``--out-timeout 10``.
        This will make the server stop searching for models with a bette cost after ``10`` seconds. Note that the response time might be larget than this timeout
        if the solver is already searching when the timeout is reached. If you pass a timeout of ``0`` the server will only get the first model, you can then keep calling the operation ``next_solution(optN)`` to improve the cost, one at a time.
        Check out the `placement_optimized example <https://github.com/potassco/clinguin/tree/master/examples/angular/placement_optimized>`_.


.. admonition:: **Can't manage to place or style things in my UI**
    :class: tip

    If you are having trouble placing or styling elements in your UI, first make sure that they are part of your UI state by checking the logs in the command line.

    *Not in my ui-state*
        If your expected attribute is not in the :ref:`ui-state`, then you have to check your :ref:`ui-files` to make sure the atom is generated.
        If you are using the ``;`` operator for the ``class`` attribute, make sure you did not make a mistake and have ``attr(elem,class,(c1,c2);`` instead of ``attr(elem,class,(c1;c2).``.

    *Is part of my ui-state*
        Then we recomend you use the browser's developer tools to inspect the elements and see if the styles are being applied.
        You can also move the HTML directly in your browser to find the right settings. Once you found them you can copy them to your :ref:`ui-files`.



.. admonition:: **Still need help**
    :class: warning

    If none of the above tips help you solve your problem, please open an issue in the `clinguin repository <https://github.com/potassco/clinguin/issues>`_.

