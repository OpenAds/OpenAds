import json
from fabric.api import *
from deployer.configuration import Configuration
from deployer.helpers import mkdir, rmdir
from deployer.standard_packages import package_list
import os
from StringIO import StringIO


site_settings = {
    "settings_module": 'OpenAds.settings',
    "settings_local": 'OpenAds/local_settings.py',
    "application_name": 'OpenAds',
    "git_location": "https://github.com/OpenAds/OpenAds.git",
    "git_branch": "develop",

    # Defaults
    "static_dir": "all_static",
    "media_dir": "media",
    "requirements_file": 'requirements.txt',
}


def load_configuration():

    with open('hosts_data.json', 'r') as f:
        configuration_file = ''.join(f.readlines())
        conf = json.JSONDecoder().decode(configuration_file)

    print "Loaded server config for {}".format(conf['server_login'])
    env.hosts.append(conf['server_login'])
    env.hosts_data = Configuration(conf, site_settings)

load_configuration()


def install_requirements():
    sudo('sudo apt-get -y update')
    sudo('sudo apt-get -y upgrade')
    sudo('sudo apt-get install -y {}'.format(package_list()))


def create_folders():
    mkdir(env.hosts_data.base_path())
    mkdir(env.hosts_data.log_path())
    sudo('sudo ln -s /usr/include/freetype2 /usr/include/freetypeserver')


def create_virtual_environment():
    with cd(env.hosts_data.base_path()):
        run('virtualenv {}'.format(env.hosts_data.virtualenv_path()))

    with prefix("source {}".format(env.hosts_data.virtualenv_activate_path())):
        run('pip install --upgrade distribute')
        run('pip install -r {}'.format(env.hosts_data.requirements_path()))
        if env.hosts_data.is_mysql():
            run('pip install mysql-python')
            run('pip install gunicorn')


def create_local_settings():
    rmdir(env.hosts_data.local_settings_path())
    put(StringIO(env.hosts_data.local_settings()), env.hosts_data.local_settings_path())


def create_gunicorn_config():
    rmdir(env.hosts_data.gunicorn_config_path())
    put(StringIO(env.hosts_data.gunicorn_config()), env.hosts_data.gunicorn_config_path())
    sudo('chmod u+x {}'.format(env.hosts_data.gunicorn_config_path()))


def create_demo_superuser():
    with cd(env.hosts_data.app_path()):
        with prefix("source {}".format(env.hosts_data.virtualenv_activate_path())):
            commands = [
                "echo \"from django.contrib.auth.models import User;",
                "User.objects.create_superuser('admin', 'admin@example.com', 'pass')\" | python manage.py shell"
            ]
            run(' '.join(commands))


def create_gunicorn_supervisor():
    rmdir(env.hosts_data.gunicorn_supervisor_config_path())
    put(
        StringIO(env.hosts_data.gunicorn_supervisor_config()),
        env.hosts_data.gunicorn_supervisor_config_path(),
        use_sudo=True
    )
    sudo('sudo supervisorctl reread')
    sudo('sudo supervisorctl update')


def create_nginx_config():
    put(StringIO(env.hosts_data.nginx_config()), env.hosts_data.nginx_available_path(), use_sudo=True)
    sudo('ln -s {} {}'.format(env.hosts_data.nginx_available_path(), env.hosts_data.nginx_enabled_path()))
    sudo('sudo service nginx restart')


def delete_nginx_config():
    rmdir(env.hosts_data.nginx_enabled_path(), sudo_access=True)
    rmdir(env.hosts_data.nginx_available_path(), sudo_access=True)
    sudo('sudo service nginx restart')


def migrate_database():
    with cd(env.hosts_data.app_path()):
        with prefix("source {}".format(env.hosts_data.virtualenv_activate_path())):
            run("python manage.py syncdb --noinput")
            run("python manage.py migrate --noinput")


def delete_folders():
    rmdir(env.hosts_data.base_path())


def delete_gunicorn_supervisor():
    server_stop()
    rmdir(env.hosts_data.gunicorn_supervisor_config_path(), sudo_access=True)
    sudo('sudo supervisorctl reread')
    sudo('sudo supervisorctl update')


def make_deploy():
    # Install all the packages
    install_requirements()

    # Create the folders for the site
    create_folders()

    # Create the git
    run(env.hosts_data.git_clone_command())
    with cd(env.hosts_data.app_path()):
        run(env.hosts_data.git_checkout_command())

    # Create the virtual environment
    create_virtual_environment()

    # Upload the local settings
    create_local_settings()

    # Create database
    migrate_database()
    create_demo_superuser()

    # Create the gunicorn environment
    create_gunicorn_config()
    create_gunicorn_supervisor()

    # Create nginx configs
    create_nginx_config()


def server_status():
    sudo('sudo supervisorctl status {}'.format(env.hosts_data.application_name()))


def server_stop():
    sudo('sudo supervisorctl stop {}'.format(env.hosts_data.application_name()))


def server_start():
    sudo('sudo supervisorctl start {}'.format(env.hosts_data.application_name()))


def server_restart():
    sudo('sudo supervisorctl restart {}'.format(env.hosts_data.application_name()))


def destroy_deploy():
    delete_folders()
    delete_gunicorn_supervisor()
    delete_nginx_config()


def update_deploy():
    server_stop()
    with cd(env.hosts_data.app_path()):
        with prefix("source {}".format(env.hosts_data.virtualenv_activate_path())):
            run('git pull')
            run('pip install -r {}'.format(env.hosts_data.requirements_path()))
    migrate_database()
    server_start()
