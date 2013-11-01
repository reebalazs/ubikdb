
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

# Monkey-patch gevent
from gevent import monkey
monkey.patch_all()


class ContextMixin(object):

    def __init__(self, *args, **kwargs):
        super(ContextMixin, self).__init__(*args, **kwargs)
        if 'rooms' not in self.session:
            self.session['contexts_recurse'] = set()  # a set of simple strings
            self.session['contexts'] = set()  # a set of simple strings

    def on_watch_context(self, context, recurse=False):
        """Lets a user join a room on a specific Namespace."""
        key = 'contexts_recurse' if recurse else 'contexts'
        self.session[key].add(self._get_context_id(context))

    def on_unwatch_context(self, context, recurse=False):
        """Lets a user leave a room on a specific Namespace."""
        key = 'contexts_recurse' if recurse else 'contexts'
        self.session[key].remove(self._get_context_id(context))

    def _get_context_id(self, context):
        return self.ns_name + '_' + context

    def emit_with_context(self, event, context, *args, **kw):
        """Send to everyone (except me) watching this context
           (in this particular Namespace)
        """
        recurse = kw.get('recurse', False)
        assert not kw or kw.keys() == ['recurse']
        pkt = dict(type="event",
                   name=event,
                   args=[context, ] + list(args),
                   endpoint=self.ns_name)
        context_name = self._get_context_id(context)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if self.socket != socket:
                if context_name in socket.session['contexts']:
                    socket.send_packet(pkt)
                elif recurse:
                    for context in socket.session['contexts_recurse']:
                        # Send this to the socket if it starts with the prefix
                        if context_name.startswith(context):
                            socket.send_packet(pkt)
                            break
                else:
                    # scan the recursive contexts too, in a non-recursive way.
                    if context_name in socket.session['contexts_recurse']:
                        socket.send_packet(pkt)


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
