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

Install with latest web-frontend
================================

Be sure that you have `make` and all the dev-tools for the web-frontend installed (`Angular`), as detailed below! Then type:

.. code-block:: bash

    $ make all

This builds the frontend, and then installs `clinguin`.


Angular (Web) Frontend Installation Guide for Development Mode
==============================================================

The following is only required for making changes to the web-frontend.

As the Angular frontend is not written in Python, but in Typescript, a different installation procedure is necessary.
The Angular installation guide can be found in `Angular <https://angular.io/guide/setup-local>`_.

For the installation you need both `Node.js <https://nodejs.org/en/download>`_ and 
the `npm-package-manager <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_,
where you can find the respective installation guide in the links.

If you have installed all the dependencies you can navigate to the `/angular-frontend` folder. There you can then type:

.. code-block:: bash

    $ ng serve

After startup the web-frontend should be (by default) displayed at `127.0.0.1:4200`.
When using the `ng serve` command you may make changes to the frontend without hitting `ng serve` again (dynamic compilation, etc.).







Starting in development mode
============================

Another possibility to run clinguin is by typing the following (-h for help):

.. code-block:: bash

    $ python start.py -h







