Configuration
=============

The ``config`` command for the ``slough`` tool can be used to manage the configuration for Slough in the current project. The following subcommands are available:

-   ``list``: list the configuration.

Listing configuration
---------------------

You can list the configuration for the current project with the subcommand ``ilst``. This gives you the ability to see what configuration is in effect. This also gives you the ability to export configuration to environment variables and use them in other programs. This can be very useful for CI/CD pipelines for example. By using the the global ``--ouput`` option, you can specify how the configuration should be outputted. For example:

.. code-block :: bash

    $ slough config list
    
      Setting                                          Value              
     ──────────────────────────────────────────────────────────────────── 
      slough.configuration.container.platforms                            
      slough.configuration.container.platforms.count   0                  
      slough.configuration.container.tags                                 
      slough.configuration.container.tags.count        0                  
      slough.project.authors.0.email                   nobody@nobody.com  
      slough.project.authors.0.name                    nobody             
      slough.project.authors.count                     1                  
      slough.project.name                              empty_project      
      slough.project.version                           0.0.1    


Or as environment variables:

.. code-block :: bash
    
    $ slough --output env config list

    SLOUGH_CONFIGURATION_CONTAINER_PLATFORMS=""
    SLOUGH_CONFIGURATION_CONTAINER_PLATFORMS_COUNT="0"
    SLOUGH_CONFIGURATION_CONTAINER_TAGS=""
    SLOUGH_CONFIGURATION_CONTAINER_TAGS_COUNT="0"
    SLOUGH_PROJECT_AUTHORS_0_EMAIL="nobody@nobody.com"
    SLOUGH_PROJECT_AUTHORS_0_NAME="nobody"
    SLOUGH_PROJECT_AUTHORS_COUNT="1"
    SLOUGH_PROJECT_NAME="empty_project"
    SLOUGH_PROJECT_VERSION="0.0.1"

You can also specify to use a specific configuration profile with the ``--profile`` option. Profiles are explained in the :doc:`profiles documentation <06-profiles>`. For example, to list the configuration for the ``dev`` profile, you can use:

.. code-block :: bash

    $ slough config list --profile dev

