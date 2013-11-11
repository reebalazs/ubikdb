
from collections import defaultdict

class ContextMixin(object):

    def __init__(self, *args, **kwargs):
        super(ContextMixin, self).__init__(*args, **kwargs)
        if 'contexts' not in self.session:
            self.session['contexts'] = defaultdict(set)
            self.session['contexts_recurse'] = defaultdict(set)

    def on_watch_context(self, context, recurse=False):
        """Lets a user watch a context on a specific namespace."""
        self.session['contexts'][self.ns_name].add(context)
        if recurse: 
            self.session['contexts_recurse'][self.ns_name].add(context)

    def on_unwatch_context(self, context):
        """Lets a user unwatch a context on a specific namespace."""
        self.session['contexts'][self.ns_name].discard(context)
        self.session['contexts_recurse'][self.ns_name].discard(context)

    def emit_in_context(self, event, context, *args):
        """Send to everyone (except me) watching this context
           (in this particular namespace)
        """
        pkt = dict(type="event",
                   name=event,
                   args=[context, ] + list(args),
                   endpoint=self.ns_name)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if self.socket != socket:
                if context in self.session['contexts'][self.ns_name]:
                    socket.send_packet(pkt)
                else:
                    for socket_context in self.session['contexts_recurse'][self.ns_name]:
                        # Send this to the socket if it starts with the prefix
                        if context.startswith(context_context):
                            socket.send_packet(pkt)
                            break
