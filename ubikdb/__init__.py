#

def initialize():
    # Monkey-patch gevent
    from gevent import monkey
    monkey.patch_all()

from .namespace import UbikDB
UbikDB = UbikDB

