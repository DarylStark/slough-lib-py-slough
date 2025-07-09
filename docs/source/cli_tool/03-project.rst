Project
=======

The ``project`` command is used to initialize a project or configure a development environment. It provides several subcommands to manage the project setup and configuration.

Subcommands
-----------

The following subcommands are available under the ``project`` command:

- ``init``: Initialize a new project.
- ``set-development=environment``: Set the development environment for the project.

Initialization
--------------

To initialize a project, you use the ``init`` subcommand for the ``project`` command. You can either specify specific values on the command line with the specific options, or you can use the interactive mode to answer the questions that are asked. The development environment can only be set with the ``--development-environment`` option, or by setting the development environment later with the ``set-development-environment`` subcommand.

An example to create a project:

.. code-block :: bash

    $ slough project init

    📛 Please enter the project title: MyAwesomeProject
    🏷️  Please enter the project version: 1.2.3
    👤 Please enter the name of the author: Daryl Stark
    📧 Please enter the email of the author: example@example.com

This will initialize a configurationfile in the current directory with the filename ``slough.yml``. This file will be used by all Slough related projects to read the configuration of the project.

Set a development environment
-----------------------------

To set a development environment, you can use the ``set-development-environment`` subcommand for the ``project`` command. After the command you have to specify the development environment you want to set. The development environment can be one of the following:

-   ``generic``
-   ``asm6502-generic``
-   ``esp32-generic``
-   ``java-generic``
-   ``nodejs-generic``
-   ``rust-generic``
-   ``cpp-generic``
-   ``lisp-scheme-generic``
-   ``python-generic``

For example:

.. code-block :: bash

    $ slough project set-development-environment python-generic
