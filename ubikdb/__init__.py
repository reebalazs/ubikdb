
# Monkey-patch gevent
from gevent import monkey
monkey.patch_all()

from .namespace import UbikDBNamespace
UbikDBNamespace = UbikDBNamespace
