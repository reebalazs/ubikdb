
from __future__ import print_function

import transaction

from transaction.interfaces import ISynchronizer
from zope.interface import implements


class Synchronizer(object):
    implements(ISynchronizer)

    # all connected instances
    instances = []

    def __init__(self):
        self.handlers = []
        self.connected = False

    def beforeCompletion(self, transaction):
        # Only run if we are the first connected sychronizer.
        # This means we are elected to propagate tha change
        # to all client.
        if self.instances.index(self) == 0:
            # First handler is enough to run.
            self.handlers[0](transaction)

    def afterCompletion(self, transaction):
        pass

    def newTransaction(self, transaction):
        pass

    def connect_synchronizer(self):
        transaction.manager.registerSynch(self)
        self.instances.append(self)
    
    def disconnect_synchronizer(self):
        self.instances.remove(self)
        transaction.manager.unregisterSynch(self)

    def on(self, f):
        self.handlers.append(f)
        if not self.connected:
            self.connect_synchronizer()
            self.connected = True
    
    def off(self, f):
        self.handlers.remove(f)
        if not self.handlers and self.connected:
            self.disconnect_synchronizer()
            self.connected = False
