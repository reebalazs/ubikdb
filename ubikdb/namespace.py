
from socketio.namespace import BaseNamespace

from .storage import StorageMixin

class UbikDBNamespace(BaseNamespace, StorageMixin):

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
