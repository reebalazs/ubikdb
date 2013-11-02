
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from .context import ContextMixin


class UbikDBNamespace(BaseNamespace, BroadcastMixin, ContextMixin):

    def __init__(self, *args, **kwargs):
        BaseNamespace.__init__(self, *args, **kwargs)
        BroadcastMixin.__init__(self)
        ContextMixin.__init__(self)

        self._root = {
            'boss': 'Glen Runciter',
            'agent': 'Joe Chip'
        }

    def on_message(self, context, msg):
        self.emit_with_context('message', context, msg, recurse=True)

    def on_norecurse(self, context, msg):
        self.emit_with_context('norecurse', context, msg)

    # --

    @property
    def root(self):
        return self._root

    def traverse_path(self, context):
        path = []
        data = self.root
        split_context = context.split('/')
        for segment in split_context:
            if segment:
                if segment in data:
                    data = data[segment]
                    path.append(data)
                else:
                    path.append(None)
                    break
        return path

    def traverse(self, context):
        return self.traverse_path(context)[-1]

    def on_get(self, context):
        value = self.traverse(context)
        return [value]

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
