
from __future__ import print_function

import transaction

from transaction.interfaces import ISynchronizer
from zope.interface import implements


class Synchronizer(object):
    implements(ISynchronizer)

    def __init__(self):
        self.handlers = []
        self.connected = False

    def beforeCompletion(self, transaction):
        # Elect the first handler to run, as it will
        # distribute the changes to all other clients too.
        if self.handlers:
            self.handlers[0](transaction)

    def afterCompletion(self, transaction):
        pass

    def newTransaction(self, transaction):
        pass

    def connect_synchronizer(self):
        print('ZODB synchronizer starts listening.')
        transaction.manager.registerSynch(self)
    
    def disconnect_synchronizer(self):
        print('ZODB synchronizer stops listening.')
        transaction.manager.unregisterSynch(self)

    def on(self, f):
        self.handlers.append(f)
        if not self.connected:
            self.connect_synchronizer()
            self.connected = True
    
    def off(self, f):
        self.handlers.remove(f)
        if not self.handlers:
            self.disconnect_synchronizer()
            self.connected = False
