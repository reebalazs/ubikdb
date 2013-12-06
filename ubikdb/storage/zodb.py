
from __future__ import print_function

import copy

from persistent import Persistent
import transaction
from transaction.interfaces import ISynchronizer
from zope.interface import (
    Interface,
    implements,
    implementer,
)
from substanced.content import content

from .storage import StorageTypeRegistry
from ..traverse import (
    traverse,
    traverse_path,
)

class IDemoContent(Interface):
    pass

@content(
    'ubikDB',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IDemoContent)
class UbikDB(Persistent):
    def __init__(self, root_key, init_content):
        self.root = {}
        self.root[root_key] = copy.deepcopy(init_content)
        self.root_key = root_key


class Synchronizer(object):
    implements(ISynchronizer)

    def beforeCompletion(self, transaction):
        pass

    def afterCompletion(self, transaction):
        print("afterCompletion", transaction)

    def newTransaction(self, transaction):
        pass


class ZODBStorage(object):

    def __init__(self, db_root, db_id='ubikdb', init_content=None):
        self.zodb_root = db_root
        self.zodb_id = db_id
        self.db_root_key = 'ubikdb'
        if self.root_key not in self.zodb_root:
            # create initial content
            if init_content is None:
                init_content = {}
            self.zodb_root[db_id] = UbikDB(self.root_key, init_content)
            transaction.commit()
        self.db_root = self.zodb_root[db_id]
        self.synchronizer = None

    def connect(self):
        self.synchronizer = Synchronizer()
        transaction.manager.registerSynch(self.synchronizer)
        
    def disconnect(self):
        transaction.manager.unregisterSynch(self.synchronizer)
        self.synchronizer = None

    @property
    def root(self):
        return self.db_root.root

    @property
    def root_key(self):
        return self.db_root_key

    def traverse_path(self, path):
        return traverse_path(self.root, self.root_key, path)

    def traverse(self, path):
        return traverse(self.root, self.root_key, path)

    def get(self, path):
        value = self.traverse(path)
        return [value]

    def set(self, path, value):
        traverse = self.traverse_path(path)
        last = traverse[-2]
        last['data'][last['segment']] = value
        self.db_root._p_changed = True
        transaction.commit()


StorageTypeRegistry.reg('zodb', ZODBStorage)
