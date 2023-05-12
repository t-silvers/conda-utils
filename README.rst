.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========
conda-utils
===========


    Helpers for working with conda (or mamba) environments.


Generating an environment file from an existing environment
====
.. Demonstrate usage of env_to_file.py with python code snippet
.. code-block:: python

    from pathlib import Path
    from conda_utils import env_to_file

    env_to_file('my-env', output_dir=Path.cwd(), overwrite=True)

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.4.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
