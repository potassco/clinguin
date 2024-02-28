Installation
############

Clinguin requires a Python version between 3.8 and 3.10 (recomend 3.10)

You can check a successfull instalaltion by running

.. code-block:: console

    $ clinguin -h

Installing with pip 
===================

The python clinguin package can be found `here <https://pypi.org/project/clinguin/>`_.

.. code-block:: console

    $ pip install clinguin

The following dependencies used in `clinguin` are optional. 

#. `tkinter`: For using the tkinter fronted.

To include them in the installation use:

.. code-block:: console

    $ pip install clinguin[tkinter]


Development
===========

Installing from source
+++++++++++++++++++++++

The project is hosted on `github <https://github.com/potassco/clinguin>`_ and can
also be installed from source. We recommend this only for development purposes.

.. note::
    The pip package `setuptools` must be previously installed

Execute the following command in the top level clinguin directory:

.. code-block:: console

    $ git clone https://github.com/potassco/clinguin
    $ cd clinguin
    $ pip install .[all]


Angular Frontend Development
++++++++++++++++++++++++++++

This section is for development and contribution in the AngularFrontend.
For instance to create new element types.


.. warning::
    
    The following is only required for making changes to the web-frontend.

Requirements
------------

    - `NPM <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_
    - `NODE <https://nodejs.org/en/download>`_
    - `Angular <https://angular.io/guide/setup-local>`_

Development
-----------

This process shows changes made on the `angular_fronted` folder in real time.

1. Start the server
    - Replace  ``clinguin client-server`` by ``python start.py server`` on the desired example
2. Start the web client
    - Open a new tab
    - Navigate to the folder `/angular_frontend`. 
    - Type ``ng serve``
    - Go to the URL `127.0.0.1:4200` in your web-browser.


Compile source code
-------------------

This allows to use the AngularFrontend by passing the ``--frontend`` argument to the client.

Be sure that you have `make` and all the dev-tools for the web-frontend installed (`Angular`), as detailed below! Then type:

.. code-block:: console

    $ make angular

This builds the frontend, and then installs `clinguin`.