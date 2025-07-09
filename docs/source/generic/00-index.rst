Slough
======

This page describes the generic idea for a Slough project. When you start a new development project, you have to do a few things:

1.  Initialize the project for the specific language or framework you are using. This can be to scaffold a specific file structure, for instance, or create a specific project tool.
2.  You add the desired tools you need to develop the project. For instance, you might need ``pre-commit``, a linting tool and a formatting tool.
3.  You start the real development for the project.
4.  You add a CI/CD pipeline to lint your project, run unit tests, bump the version and release the project. You might need to create a containerimage and publish it. The details for this might differ for specific branches.

To do this every time you start a new project is ridicilous. The Slough project is created to minimalize these steps for you. Slough defines one simple config file that you put inside your project root folder. This configfile contains your project details. When you have created this file, you can generate the configurationfiles for a Slough dev container in which the required tools are already installed. It also gives you the ability to export your configuration to the environment, so your CI/CD tools can use the correct information.

The Slough configuration file is split into different profiles; each profile can have different configuration. This way, you can, for instance, creaet different configuration for development, acceptance and production.

The Slough project contains a few components:

-   Various dev containers for specific languages and frameworks:
    -   Python
    -   NodeJS
    -   Rust
    -   Java
    -   C++
    -   ESP-IDF
    -   LISP
    -   ASM for the MOS 6502
-   A CLI tool to configure your project.
-   A few GitHub actions to run your CI/CD pipeline.
-   A few GitHub workflows to use for your projects.