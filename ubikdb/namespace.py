
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
        traverse = [dict(data=self.root)]
        split_context = context.split('/')
        for segment in split_context:
            last = traverse[-1]
            data = last['data']
            if segment:
                last['segment'] = segment
                if segment in data:
                    data = data[segment]
                    traverse.append(dict(data=data))
                else:
                    traverse.append(dict(data=None))
                    break
        return traverse

    def traverse(self, context):
        return self.traverse_path(context)[-1]['data']

    def on_get(self, context):
        value = self.traverse(context)
        return [value]

    def on_set(self, context, value):
        traverse = self.traverse_path(context)
        if len(traverse) == 1:
            print "on_set /", value
            self.root = value
        else:
            last = traverse[-2]
            print "on_set", context, last
            last['data'][last['segment']] = value
        # notify listeners
        self.emit_with_context('set', context, value, recurse=True)

    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)
