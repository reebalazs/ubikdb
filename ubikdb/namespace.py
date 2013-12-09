
from socketio.namespace import BaseNamespace

from .storage import StorageMixin

class UbikDB(BaseNamespace, StorageMixin):

    def recv_connect(self):
        StorageMixin.recv_connect(self)

    def recv_disconnect(self):
        StorageMixin.recv_disconnect(self)
        self.disconnect(silent=True)
