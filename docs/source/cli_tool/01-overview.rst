CLI tool overview
=================

You can start the CLI tool by using the command `slough`. If you enter it without any arguments, or with the ``--help`` argument, you get a generic help for the command:

.. code-block:: bash

   $ slough

   Usage: slough [OPTIONS] COMMAND [ARGS]...

   Common options for all commands.
   This is run for all commands, and makes sure the correct configuration file is loaded.
   Args:     ctx (typer.Context): Typer context object.     cfgfile (str): Path to the configuration file.
   verbosity (int): Verbosity level.     output (OutputType): Output format.

   ╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --verbosity           -v      INTEGER RANGE [x<=2]        Increase output verbosity. [default: 0]             │
   │ --output                      [console|env|exported-env]  Output format. [default: console]                   │
   │ --install-completion                                      Install completion for the current shell.           │
   │ --show-completion                                         Show completion for the current shell, to copy it   │
   │                                                           or customize the installation.                      │
   │ --help                                                    Show this message and exit.                         │
   ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ version         Print version.                                                                                │
   │ config          Configuration related commands.                                                               │
   │ project         Project related commands.                                                                     │
   │ dev-container   Dev container commands.                                                                       │
   │ container       Container commands.                                                                           │
   │ profiles        Configuration profiles.                                                                       │
   ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

To get the current version for the ``slough`` CLI tool, give the ``version`` command:

.. code-block:: bash

    $ slough version
    Slough CLI 1.0.0-beta.7

There are several sections in the ``slough`` CLI tool that you can use:

-   ``config``: the manage configuration (:doc:`documentation <02-config>`)
-   ``project``: to initialize a project or configurate a development environment (:doc:`documentation <03-project>`)
-   ``dev-container``: to generate the needed configuration for a development container (:doc:`documentation <04-dev-container>`)
-   ``container``: to set options for container configuration (:doc:`documentation <05-container>`)
-   ``profiles``: to manage configuration profiles (:doc:`documentation <06-profiles>`)