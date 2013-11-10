

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
        return self.ns_name + ':' + context

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
                if context_name in self.session['contexts']:
                    socket.send_packet(pkt)
                elif recurse:
                    for context in self.session['contexts_recurse']:
                        # Send this to the socket if it starts with the prefix
                        if context_name.startswith(context):
                            socket.send_packet(pkt)
                            break
                else:
                    # scan the recursive contexts too, in a non-recursive way.
                    if context_name in self.session['contexts_recurse']:
                        socket.send_packet(pkt)
