
from transaction.interfaces import ISynchronizer
from zope.interface import implements


class Synchronizer(object):
    implements(ISynchronizer)

    def __init__(self, storage):
        self.storage = storage

    def beforeCompletion(self, transaction):
        self.storage.before_completion(transaction)

    def afterCompletion(self, transaction):
        pass

    def newTransaction(self, transaction):
        pass
