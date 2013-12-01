
from .traverse import traverse

class EventRegistry(object):

    SESSION_KEY = 'context_mixin'

    def __init__(self):
        self.target = set()
        self.parent = set()
        self.children = set()

    @classmethod
    def reg(cls, socket, ns_name):
        store = socket.session.setdefault(cls.SESSION_KEY, {})
        try:
            return store[ns_name]
        except KeyError:
            result = store[ns_name] = EventRegistry()
            return result

class ContextMixin(object):

    def __init__(self, *args, **kwargs):
        super(ContextMixin, self).__init__()

    @property
    def reg(self):
        return EventRegistry.reg(self.socket, self.ns_name)

    def on_watch_context(self, path, recurse=None):
        """Lets a user watch a context on a specific namespace."""
        self.reg.target.add(path)
        if recurse:
            if 'parent' in recurse: 
                self.reg.parent.add(path)
            if 'children' in recurse: 
                self.reg.children.add(path)

    def on_unwatch_context(self, path):
        """Lets a user unwatch a context on a specific namespace."""
        self.reg.target.discard(path)
        self.reg.parent.discard(path)
        self.reg.children.discard(path)

    def emit_in_context(self, event, path, *args):
        """Send to everyone (except me) watching this context
           (in this particular namespace)
        """
        pkt = dict(
            type="event",
            name=event,
            args=[path, ] + list(args),
            endpoint=self.ns_name,
        )
        for sessid, socket in self.socket.server.sockets.iteritems():
            if self.socket != socket:
                reg = EventRegistry.reg(socket, self.ns_name)
                if path in reg.target:
                    socket.send_packet(pkt)
                else:
                    for watch in reg.parent:
                        # Send this to the socket if it starts with the prefix
                        if path.startswith(watch):
                            socket.send_packet(pkt)
                            break
                    # Sending individual fragments to children.
                    # Collect the interests.
                    watches = set()
                    for watch in reg.children:
                        if watch.startswith(path):
                            # add this watch and shorten existing ones
                            for already in list(watches):
                                if watch.startswith(already):
                                    watches.remove(already)
                                elif already.startswith(watch):
                                    break
                            else:
                                watches.add(watch)
                    # Emit individual packets for each interesting watch.
                    # First arg is always the data
                    data = args[0] if args else {}
                    for watch in watches:
                        path = watch.substring(path.length, watch.length)
                        traversed = traverse(data, path)
                        trim_data = traversed[-1].data
                        trim_pkt = dict(
                            type="event",
                            name=event,
                            args=[watch, trim_data] + args[1:],
                            endpoint=self.ns_name,
                        )
                        socket.send_packet(trim_pkt)
