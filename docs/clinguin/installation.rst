Installation
############

Clinguin Installation guide:

Current installation procedure
===============================


You need to have a working `python` installation (version 3.10 is recommended) and also the pip package `setuptools` installed. Then the current recommended way to install clinguin is to execute the following command in the top level clinguin directory:

.. code-block:: bash

    $ python -m pip install ./ 

If you want to have the tkinter gui you need the `tkinter` dependency, which can be installed in one step together with clinguin:

.. code-block:: bash

    $ python -m pip install ./[tkinter]

If you want to have the full dependencies of the development environment you can install clinguin in the following way:

.. code-block:: bash

    $ python -m pip install ./[tkinter,doc]

After this, one can run clinguin by executing (-h for help):

.. code-block:: bash

    $ clinguin -h


Starting in development mode
============================

Another possibility to run clinguin is by typing the following (-h for help):

.. code-block:: bash

    $ python start.py -h







