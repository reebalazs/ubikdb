
from collections import defaultdict
from .traverse import traverse

class ContextMixin(object):

    def __init__(self, *args, **kwargs):
        super(ContextMixin, self).__init__(*args, **kwargs)
        if 'contexts' not in self.session:
            self.session['contexts'] = defaultdict(set)
            self.session['contexts_parent'] = defaultdict(set)
            self.session['contexts_children'] = defaultdict(set)

    def on_watch_context(self, context, recurse={}):
        """Lets a user watch a context on a specific namespace."""
        self.session['contexts'][self.ns_name].add(context)
        if recurse.get('parent', False): 
            self.session['contexts_parent'][self.ns_name].add(context)
        if recurse.get('children', False): 
            self.session['contexts_children'][self.ns_name].add(context)

    def on_unwatch_context(self, context):
        """Lets a user unwatch a context on a specific namespace."""
        self.session['contexts'][self.ns_name].discard(context)
        self.session['contexts_parent'][self.ns_name].discard(context)
        self.session['contexts_children'][self.ns_name].discard(context)

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
                if context in socket.session['contexts'][self.ns_name]:
                    socket.send_packet(pkt)
                else:
                    for watch in socket.session['contexts_parent'][self.ns_name]:
                        # Send this to the socket if it starts with the prefix
                        if context.startswith(watch):
                            socket.send_packet(pkt)
                            break
                    # Sending individual fragments to children.
                    # Collect the interests.
                    watches = set()
                    for watch in socket.session['contexts_children'][self.ns_name]:
                        if watch.startswith(context):
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
                        path = watch.substring(context.length, watch.length)
                        traversed = traverse(data, path)
                        trim_data = traversed[-1].data
                        trim_pkt = dict(type="event",
                           name=event,
                           args=[watch, trim_data] + args[1:],
                           endpoint=self.ns_name)
