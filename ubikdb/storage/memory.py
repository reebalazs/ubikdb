
import copy
from .storage import StorageTypeRegistry
from ..traverse import traverse_getset


class MemoryStorage(object):

    root = {}
    root_key = 'ubikdb'
    
    def set_notify_changes(self, callback):
        pass

    def connect(self, callback):
        pass

    def disconnect(self, callback):
        pass

    def get(self, path):
        return traverse_getset(self.root, (self.root_key, path))

    def set(self, path, value):
        traverse_getset(self.root, (self.root_key, path), value, set=True)

StorageTypeRegistry.reg('memory', MemoryStorage)


class SandboxStorage(MemoryStorage):

    def __init__(self, sandbox_content=None):
        super(SandboxStorage, self).__init__()
        if sandbox_content is None:
            sandbox_content = {}
        if self.root_key not in self.root:
            self.root[self.root_key] = copy.deepcopy(sandbox_content)

StorageTypeRegistry.reg('sandbox', SandboxStorage)
