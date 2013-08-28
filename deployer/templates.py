LOCAL_SETTINGS = """DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.{type}',
        'NAME': '{name}',

        # The following settings are not used with sqlite3:
        'USER': '{user}',
        'PASSWORD': '{password}',
        'HOST': '{host}',
        'PORT': '',
    }}
}}

ALLOWED_HOSTS = ['{site_name}']

DEBUG = False
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ADMINS = (
{admins}
)

{additional_settings}
"""

ADDITIONAL_SETTINGS_FORMAT = "{setting_name} = {setting_value}\n"
ADMIN_SETTINGS_FORMAT = "    ('{admin_name}', '{admin_email}'),\n"

GUNICORN_START = """#!/bin/bash

NAME="{app_name}"                                  # Name of the application
DJANGODIR={app_dir}             # Django project directory
SOCKFILE={socket}  # we will communicte using this unix socket
USER={user}                                       # the user to run as
GROUP={user}                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE={settings}             # which settings file should Django use


echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source {activate}
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec {gunicorn_bin} \\
  --name $NAME \\
  --workers $NUM_WORKERS \\
  --user=$USER --group=$GROUP \\
  --log-level=debug \\
  --bind=unix:$SOCKFILE
"""

GUNICORN_SUPERVISOR = """
[program:{app_name}]
command = {gunicorn_start}                                            ; Command to start app
user = {user}                                                         ; User to run as
stdout_logfile = {gunicorn_log}                                       ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
"""

NGINX_CONFG = """
upstream {app_name}_app_server {{
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:{socket} fail_timeout=0;
}}

server {{

    listen   80;
    server_name {site_name};

    client_max_body_size 4G;

    access_log {access_log};
    error_log {error_log};

    location /static/ {{
        alias   {static}/;
    }}

    location /media/ {{
        alias   {media}/;
    }}

    location / {{
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f $request_filename) {{
            proxy_pass http://{app_name}_app_server;
            break;
        }}
    }}
}}
"""