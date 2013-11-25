
from socketio.namespace import BaseNamespace

from .context import ContextMixin
from .storage import StorageMixin

class UbikDBNamespace(BaseNamespace, StorageMixin, ContextMixin):

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
