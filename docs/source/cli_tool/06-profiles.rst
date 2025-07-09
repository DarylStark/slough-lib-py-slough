Profiles
========

Profiles are a very important part for Slough; they define a specific environment with custom settings. There are two predefined profiles:

-   ``_default``
-   ``_all``

Everything that you put in the ``_default`` profile are settings that you can use without any ``--profile`` command. This is therefor the default profile. The ``_all`` profile is a profile that will always be used for any profile. If you specify a containertag of ``latest`` in your ``_all`` profile, for instance, this tag will always be applied, no matter what profile is chosen.

The ``profiles`` subcommand for ``slough`` can be used to manage profiles. You have several subcommands:

-   ``add``; add a profile
-   ``list``; list all created profiles
-   ``remove``; remove a profile
-   ``rename``; rename a profile