
from .storage import StorageTypeRegistry
from ..traverse import (
    traverse,
    traverse_path,
)


class ZODBStorage(object):

    def __init__(self):
        self.db_root = {}
        self.db_root_key = 'ubikdb'
        self.root[self.root_key] = {
            'boss': 'Glen Runciter',
            'agent': 'Joe Chip',
            'salary': [
                {'name': 'Glen Runciter', 'value': 1000},
                {'name': 'Joe Chip', 'value': 900},
            ],
        }

    def connect(self):
        pass
        
    def disconnect(self):
        pass

    @property
    def root(self):
        return self.db_root

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

StorageTypeRegistry.reg('zodb', ZODBStorage)
