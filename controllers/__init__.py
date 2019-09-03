__all__ = ["v1"]
from .v1 import v1_installer

def install_controllers(app, prefix):
    v1_installer(app, prefix + '/v1')
    