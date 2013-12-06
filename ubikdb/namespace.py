
from socketio.namespace import BaseNamespace

from .storage import StorageMixin

class UbikDB(BaseNamespace, StorageMixin):

    def recv_connect(self):
        print "connect", self
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
