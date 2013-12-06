
from .storage import StorageTypeRegistry
from ..traverse import (
    traverse,
    traverse_path,
)


class MemoryStorage(object):

    def __init__(self):
        self.db_root = {}
        self.db_root_key = 'ubikdb'
        # initialize with static example content
        self.root[self.root_key] = {}
    
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

StorageTypeRegistry.reg('memory', MemoryStorage)
StorageTypeRegistry.DEFAULT_STORAGE_TYPE = 'memory'


class SandboxStorage(MemoryStorage):

    def __init__(self, sandbox_content=None):
        super(SandboxStorage, self).__init__()
        if sandbox_content is None:
            sandbox_content = {}
        self.root[self.root_key] = sandbox_content

StorageTypeRegistry.reg('sandbox', SandboxStorage)
