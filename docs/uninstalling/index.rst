Uninstallation guide
====================

Uninstalling is made simple as you only need to execute one command. The uninstall performs the following:

#. Stops the gunicorn server
#. Uninstalls the supervisor configuration
#. Restarts supervisor
#. Uninstalls the nginx configuration
#. Reloads nginx
#. Removes the directory at which the program is located at

The command to run on your **local machine** is::

   fab destroy_deploy

After the command has finished running, the site will be gone.

.. note::
   The database will **not** be cleared during uninstallation. If you want to empty the database, you must perform
   this manually.

