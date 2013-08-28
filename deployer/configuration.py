import os
from deployer.templates import (
    LOCAL_SETTINGS,
    GUNICORN_START,
    GUNICORN_SUPERVISOR,
    NGINX_CONFG,
    ADDITIONAL_SETTINGS_FORMAT,
    ADMIN_SETTINGS_FORMAT
)


class Configuration(object):

    def __init__(self, data_to_load, site_settings):
        self.data = data_to_load
        self.site_settings = site_settings

    def settings_module(self):
        return self.site_settings["settings_module"]

    def application_name(self):
        return self.site_settings["application_name"]

    def user(self):
        return self.data["deploy_settings"]["deploy_user"]

    def site_name(self):
        return self.data["website_url"]

    def base_path(self):
        return self.data["deploy_settings"]["deploy_to"]

    def log_path(self):
        return os.path.join(self.base_path(), self.data["deploy_settings"]["deploy_log_folder"])

    def app_path(self):
        return os.path.join(self.base_path(), self.application_name())

    def static_path(self):
        return os.path.join(self.app_path(), self.site_settings["static_dir"])

    def media_path(self):
        return os.path.join(self.app_path(), self.site_settings["media_dir"])

    def git_clone_command(self):
        return "git clone {} {}".format(self.site_settings["git_location"], self.app_path())

    def git_branch(self):
        return self.site_settings["git_branch"]

    def git_checkout_command(self):
        return "git checkout {}".format(self.git_branch())

    def virtualenv_path(self):
        return os.path.join(self.base_path(), self.data["deploy_settings"]["deploy_virtualenv_dir"])

    def virtualenv_activate_path(self):
        return os.path.join(self.virtualenv_path(), 'bin/activate')

    def requirements_path(self):
        return os.path.join(self.app_path(), self.site_settings["requirements_file"])

    def database_type(self):
        return self.data["database"]["type"]

    def is_mysql(self):
        if self.database_type() == 'mysql':
            return True
        return False

    def local_settings(self):

        additional_settings = ""
        for setting in self.data["other_settings"]:

            setting_value = self.data["other_settings"][setting]
            if type(setting_value) == str or type(setting_value) == unicode:
                setting_value = "'" + setting_value + "'"

            additional_settings += ADDITIONAL_SETTINGS_FORMAT.format(
                setting_name=setting.upper(),
                setting_value=setting_value
            )
        additional_settings = additional_settings.strip('\n')

        admins = ""
        for admin in self.data["admins"]:
            admins += ADMIN_SETTINGS_FORMAT.format(
                admin_name=admin,
                admin_email=self.data["admins"][admin]
            )
        admins = admins.strip('\n')

        return LOCAL_SETTINGS.format(
            name=self.data["database"]["name"],
            host=self.data["database"]["host"],
            user=self.data["database"]["user"],
            password=self.data["database"]["pass"],
            type=self.database_type(),
            site_name=self.site_name(),
            additional_settings=additional_settings,
            admins=admins
        )

    def local_settings_path(self):
        return os.path.join(self.app_path(), self.site_settings["settings_local"])

    def gunicorn_socket_path(self):
        return os.path.join(self.base_path(), self.data["deploy_settings"]["deploy_gunicorn_socket"])

    def gunicorn_bin_path(self):
        return os.path.join(self.virtualenv_path(), 'bin/gunicorn_django')

    def gunicorn_config(self):
        return GUNICORN_START.format(
            app_name=self.application_name(),
            app_dir=self.app_path(),
            socket=self.gunicorn_socket_path(),
            user=self.user(),
            settings=self.settings_module(),
            activate=self.virtualenv_activate_path(),
            gunicorn_bin=self.gunicorn_bin_path(),
        )

    def gunicorn_config_path(self):
        return os.path.join(self.base_path(), self.data["deploy_settings"]["deploy_gunicorn_starter"])

    def gunicorn_supervisor_config(self):
        return GUNICORN_SUPERVISOR.format(
            app_name=self.application_name(),
            user=self.user(),
            gunicorn_start=self.gunicorn_config_path(),
            gunicorn_log=os.path.join(self.log_path(), 'gunicorn_supervisor.log')
        )

    def supervisor_name(self):
        return self.application_name() + '.conf'

    def gunicorn_supervisor_config_path(self):
        return os.path.join(self.data["deploy_settings"]["deploy_supervisor"], self.supervisor_name())

    def nginx_config(self):
        return NGINX_CONFG.format(
            app_name=self.application_name(),
            socket=self.gunicorn_socket_path(),
            site_name=self.site_name(),
            access_log=os.path.join(self.log_path(), 'access.log'),
            error_log=os.path.join(self.log_path(), 'error.log'),
            static=self.static_path(),
            media=self.media_path(),
        )

    def nginx_base_path(self):
        return self.data["deploy_settings"]["deploy_nginx"]

    def nginx_conf_name(self):
        return self.site_name() + '.conf'

    def nginx_available_path(self):
        return os.path.join(self.nginx_base_path(), 'sites-available', self.nginx_conf_name())

    def nginx_enabled_path(self):
        return os.path.join(self.nginx_base_path(), 'sites-enabled', self.nginx_conf_name())
