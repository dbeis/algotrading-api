from .v1 import v1_installer

def install_controllers(prefix):
    v1_installer(prefix + '/v1')
    