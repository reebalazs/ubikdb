
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

    #def on_message(self, context, msg):
    #    self.emit_with_context('message', context, msg, recurse=True)

    #def on_norecurse(self, context, msg):
    #    self.emit_with_context('norecurse', context, msg)

    # --

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
