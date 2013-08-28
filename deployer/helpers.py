from fabric.api import *


def mkdir(folder, sudo_access=False):
    if sudo:
        sudo('mkdir -p {}'.format(folder))
    else:
        run('mkdir -p {}'.format(folder))


def rmdir(folder, sudo_access=False):
    if sudo_access:
        sudo('rm -rf {}'.format(folder))
    else:
        run('rm -rf {}'.format(folder))
