Installation
############

Clinguin requires a Python version between 3.8 and 3.10, we recomend 3.10

.. warning:: 
    For using the Angular web fronted additional steps must be followed see :ref:`syntax <angular>`

You can check a successfull instalaltion by running

.. code-block:: bash

    $ clinguin -h


Installing with conda
=====================

The conda clinguin package can be found `here <https://anaconda.org/potassco/clinguin>`_.

.. code-block:: bash

    $ conda install -c potassco clinguin 
    $ conda install -c potassco/label/dev clinguin

.. note::
    The conda installation does not include optional dependencies for tkinter. 

    .. code-block:: bash

        $ conda install -c conda-forge tk
        


Installing with pip 
===================

The python clinguin package can be found `here <https://pypi.org/project/clinguin/>`_.



.. code-block:: bash

    $ pip install clinguin

The following dependencies used in `clinguin` are optional. 

#. `tkinter`: For using the tkinter fronted.

To include them in the installation use:

.. code-block:: bash

    $ pip install clinguin[tkinter]


Installing from source
======================

The project is hosted on github at https://github.com/potassco/clinguin and can
also be installed from source. We recommend this only for development purposes.

.. note::
    The pip package `setuptools` must be previously installed

Execute the following command in the top level clinguin directory:

.. code-block:: bash

    $ git clone https://github.com/potassco/clinguin
    $ cd clinguin
    $ pip install .[all]


Angular (Web) Frontend
======================

TODO make this simpler with conda and pip


Basic installation
------------------

Be sure that you have `make` and all the dev-tools for the web-frontend installed (`Angular`), as detailed below! Then type:

.. code-block:: bash

    $ make all

This builds the frontend, and then installs `clinguin`.


Angular (Web) Frontend Installation Guide for Development Mode
---------------------------------------------------------------

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
When using the `ng serve` command you may make changes to the frontend without hitting `ng serve` again getting a dynamic compilation.







Starting in development mode
============================

Another possibility to run clinguin is by typing the following (-h for help):

.. code-block:: bash

    $ python start.py -h








## Web-Frontend Build and Deploy

1. (Optional) Manually build: `make all`
2. For e.g. the housing example you can type: 
```
clinguin client-server --domain-files examples/clingo/housing/instance.lp examples/clingo/housing/encoding.lp --ui-files examples/clingo/housing/ui.lp  --server-port 8000 --frontend AngularFrontend --client-port 8087
```
3. Then navigate in the browser of your choice to `127.0.0.1:8087` and enjoy :-)


### Details

Use the lines of code from the `Makefile`, i.e.:

```
pushd angular_frontend/; ng build; popd
mv angular_frontend/dist/clinguin_angular_frontend clinguin/client/presentation/frontends/angular_frontend
```

First `ng build` is executed, which builds the application in the `/angular_frontend/dist/clinguin_angular_frontend` folder.
This folder is then moved to `/clinguin/client/presentation/frontends/angular_frontend`. 
The corresponding clinguin frontend, `angular_frontend.py`, starts a web-server which serves our angular frontend.

To facilitate the options of different ports, the `--server-port` option specifies the port of the backend, when either using `client-server` or `server`.

When using the `--frontend AngularFrontend` frontend (`client-server` or `client`), one can always set the `--client-port` to specify the port of the webserver, which one accesses through the browser.
For `client` the additional `--server-url` and `--server-port` options let one specify the location of the server, when the server is e.g. on another machine than the client.

## Web-Frontend Development Enviroment

This option show changes made on the `angular_fronted` folder in real time.


- Needed:
    - NPM/Node (default web-development setup):  [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), [NODE](https://nodejs.org/en/download)
    - Angular: ([installation page](https://angular.io/guide/setup-local))

1. Start the server
    - Replace  `clinguin client-server` by `python start.py server` and remove argument `--frontend=AngularFrontend` from the command line of the desired example
2. Start the web client
    - Open a new tab
    - Navigate to the folder `/angular_frontend`. 
    - Type `ng serve`
    - Go to the URL `127.0.0.1:4200` in your web-browser.