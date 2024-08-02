Contributing
============

To improve code quality, we use nox to run linters, type checkers, unit
tests, documentation and more. We recommend installing nox using pipx to have
it available globally.

.. code-block:: console

    # install
    python -m pip install pipx
    python -m pipx install nox

    # run all sessions
    nox

    # list all sessions
    nox -l

    # run individual session
    nox -s session_name

    # run individual session (reuse install)
    nox -Rs session_name

Note that the nox sessions create [editable] installs. In case there are issues,
try recreating environments by dropping the `-R` option. If your project is
incompatible with editable installs, adjust the `noxfile.py` to disable them.


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
