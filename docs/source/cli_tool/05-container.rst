Container
=========

The ``container`` command is used to manage settings for when you want to create a container image. Imagine you are creating a piece of software that is going to be containerized. You want to use a generic pipeline that doesn't contain any configuration for the container, because that would kill the reusability of the pipeline. Instead, the containerimage configuration should go into a seperate file. The ``slough`` tool can do that just for you.

Configuration options
---------------------

Right now, there are two configuration options available for the ``container`` command:

-   ``registry``; the registry where the container image should be pushed to. This can be ``https://docker.io``, ``https://ghcr.io`` or any other registry that you want to use. This can also be a local registry.
-   ``image``; the name of the image that should be created. This is the name that you will use to refer to the image in your pipeline. It can be any name that you want, but it is recommended to use a name that is unique and descriptive.

To set these options, you use the ``slough container set <setting> <value>`` command. For example, to set the registry to ``https://docker.io``, you would run:

.. code-block :: bash

    $ slough container set registry https://docker.io
    $ slough container set image my-image

If you want to set the options for a specific configuration profile, you can use the ``--profile`` option. By default, this is set to the ``_default`` profile.

Tags
----

You can specify what tags should be used for the container image. This is done by using the ``slough container tags`` subcommand. You have several subcommands to this subcommand:

-   ``add``; add a tag to the container image.
-   ``remove``; remove a tag from the container image.
-   ``list``; list all tags for the container image.

By giving a profile with ``--profile``, you can specify for what profile the tags are added. This way, you can add specific tags to, for instance, only production or development branches.

Platforms
---------

You can specify for what platforms the image has to be build. This is done by using the ``slough container platforms`` subcommand. You have several subcommands to this subcommand:


-   ``add``; add a platform to the container image.
-   ``remove``; remove a platform from the container image.
-   ``list``; list all configured platforms for the container image.

By giving a profile with ``--profile``, you can specify for what profile the platforms are added. This way, you can add specific platforms to, for instance, only production or development branches.