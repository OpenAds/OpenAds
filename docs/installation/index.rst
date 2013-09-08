############
Installation
############

The whole server is relatively easy to set up on most servers. It uses the following to run:

#. Gunicorn as the server for the site
#. Nginx as a proxy server to manage the load

This system uses `Fabric <http://docs.fabfile.org/en/1.7/>`_ to deploy, which means relatively low work to get the
system up and running. All configurations are generated automatically and required packages installed.

.. warning::
   All commands should be run on your **local machine** unless specifically stated. The automated setup will
   deal with SSHing into your machine and running the commands for you.

Requirements
------------

The projects requires `Python 2.7+ <http://www.python.org/download/releases/2.7/>`_

For the automated setup, you need to be running either Debian or Ubuntu. You can run the site on other
operating systems, though the automatic installer will not work.

Getting the source code
-----------------------

Clone the source code to you **local machine** first by running the following command in bash::

   git clone https://github.com/OpenAds/OpenAds.git open_ads

Once it has finished cloning, install fabric into your python packages::

   pip install fabric

Go into the :file:`open_ads` folder and edit the :file:`hosts_data.json` file with the required settings.

The :file:`hosts_data.json` file should look similar to the following:

.. code-block:: javascript

   {
       "server_login": "localhost",
       "website_url": "localhost:8000",

       "database": {
           "type": "mysql",
           "host": "localhost",
           "name": "db",
           "user": "root",
           "pass": ""
       },

       "deploy_settings": {
           "deploy_to": "/var/openads",
           "deploy_user": "root",
           "deploy_nginx": "/etc/nginx",
           "deploy_supervisor": "/etc/supervisor/conf.d",
           "deploy_log_folder": "logs",
           "deploy_gunicorn_socket": "gunicorn.sock",
           "deploy_gunicorn_starter": "gunicorn_start",
           "deploy_virtualenv_dir": "env"
       },

       "other_settings": {
           "email_host": "localhost",
           "email_host_user": "username",
           "email_host_password": "password",
           "default_from_email": "from@example.com",
           "email_port": 25,
           "email_use_tls": false
       },

       "admins":{
           "Admin Name": "email@example.com",
           "Bdmin Name": "tests@example.com"
       }
   }

.. note::
   You should not need to copy the above, as the :file:`hosts_data.json` file should already exist.

Website name setup
------------------

In the :file:`hosts_data.json` file, there are two settings up the top. The first is ``server_login`` and
the second is ``website_url``. The ``website_url`` directive should contain the hostname that points
to your server's IP address. This is the only URL that the site will be accessible at. Some examples of valid
site names are::

   mysite.com
   sub.mysite.com
   www.mysite.com

The second setting, ``server_login``, is the SSH address for your server. You must have SSH access to your
server for the automated setup to work. Some examples of valid server logins are::

   root@mysite.com
   user@example.com
   root@mysite.com:2222

Database Setup
--------------

In the database section, enter the appropriate settings to connect to your database.

.. code-block:: javascript

   "database": {
       "type": "mysql",
       "host": "localhost",
       "name": "db",
       "user": "root",
       "pass": ""
   },

.. warning::
   The database must exist before the setup starts, or it will fail

Deploy Settings
---------------

These settings are only for more customisation, or if you do not have the standard configuration paths
for your programs. You should normally not need to modify these.

Email Settings
--------------

To be able to receive email alerts when servers go down and come back online, you must set the 
correct SMTP settings under ``other_settings``.

.. code-block:: javascript

   "other_settings": {
       "email_host": "localhost",
       "email_host_user": "username",
       "email_host_password": "password",
       "default_from_email": "from@example.com",
       "email_port": 25,
       "email_use_tls": false
   },

If your server uses SSL, you must set ``email_use_tls`` to ``true`` and possibly change the port
(if your provider has SSL on a different port)

All the settings here should be fairly self-explanatory.

Admins
------

These are the people who are emailed when the server suffers from a critical error. If you do not need this,
leave the ``admins`` setting empty, like the following:

.. code-block:: javascript

   "admins":{}

If you do leave it on and receive errors, please notify us of those errors as they are usually related to
bugs in the code.

Deploying the site
------------------

Now that the :file:`hosts_data.json` file is configured with your data, you can finally deploy your site.
Ensure that you are in the main directory of the code, and run::

   fab make_deploy

This will setup all required files, install a supervisor configuration and load in a new site to nginx.
At times during the install you may be asked for your root password to install packages.

The site is now installed, and you can navigate to your domain name that you set with ``website_url``
and use the site. A demo user has been installed with an insecure password which you must change as soon
as you login. The demo user's details are:

| **Username:** user
| **Password:** pass

Example configuration
---------------------

.. code-block:: javascript

   {
       "server_login": "root@my.server.com",
       "website_url": "mysite.com",

       "database": {
           "type": "mysql",
           "host": "localhost",
           "name": "database_name",
           "user": "database_user",
           "pass": "database_password"
       },

       "deploy_settings": {
           "deploy_to": "/var/openads",
           "deploy_user": "root",
           "deploy_nginx": "/etc/nginx",
           "deploy_supervisor": "/etc/supervisor/conf.d",
           "deploy_log_folder": "logs",
           "deploy_gunicorn_socket": "gunicorn.sock",
           "deploy_gunicorn_starter": "gunicorn_start",
           "deploy_virtualenv_dir": "env"
       },

       "other_settings": {
           "email_host": "localhost",
           "email_host_user": "management",
           "email_host_password": "password",
           "default_from_email": "management@example.com",
           "email_port": 25,
           "email_use_tls": false
       },

       "admins":{
           "Bill Short": "email@example.com",
       }
   }

