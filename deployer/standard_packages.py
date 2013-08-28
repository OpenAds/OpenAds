from fabric.api import *

REQUIRED_SYSTEM_PACKAGES = [
    'gcc',
    'python-dev',
    'python-pip',
    'libjpeg-dev',
    'libfreetype6-dev',
    'git',
    'nginx',
    'python-virtualenv',
    'libxml2-dev',
    'libmysqlclient-dev',
    'supervisor',
]


def package_list():
    return ' '.join(REQUIRED_SYSTEM_PACKAGES)