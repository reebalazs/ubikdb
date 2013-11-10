
from socketio.namespace import BaseNamespace

from .context import ContextMixin
from .storage import StorageMixin

# Database is kept in memory (volatile)
global db_root
db_root = {}
db_root_key = 'ubikdb'
db_root[db_root_key] = {
    'boss': 'Glen Runciter',
    'agent': 'Joe Chip'
}


class UbikDBNamespace(BaseNamespace, StorageMixin, ContextMixin):

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
