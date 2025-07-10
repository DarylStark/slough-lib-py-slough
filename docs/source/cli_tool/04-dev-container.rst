Dev container
=============

After you have configured your project, you can generate the config files for a dev container. A dev container is a Docker container in which all the required tools are installed. A lot of IDEs support to work inside of a dev container. To use a dev container, your project needs specific files. The ``slough`` tool can generate these files for you and pick out a image file that suits the given development environment.

To generate a dev container, first make sure that a development environment is set with ``slough project set-development-environment``. After that, you can easily generate the dev container configuration with:

.. code-block:: bash

    $ slough dev-container generate-config

You can optionally specify a specific tag with ``--container-tag``. You can also specify that a Docker socket should be mounted with ``--bind-docker-socket``. This is useful if you need to work with the local Docker installation from within the dev container.