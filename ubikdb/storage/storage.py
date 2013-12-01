
from __future__ import print_function

from ..context import ContextMixin
from ..traverse import (
    traverse,
    traverse_path,
)

# Database is kept in memory (volatile)
global db_root
db_root = {}
db_root_key = 'ubikdb'
db_root[db_root_key] = {
    'boss': 'Glen Runciter',
    'agent': 'Joe Chip',
    'salary': [
        {'name': 'Glen Runciter', 'value': 1000},
        {'name': 'Joe Chip', 'value': 900},
    ]
}

class StorageTypeRegistry(object):

    storage_classes = {}
    DEFAULT_STORAGE_TYPE = None

    @classmethod
    def reg(cls, name, storageClass):
        if name in cls.storage_classes:
            raise RuntimeError('Cannot register storage twice [%(name)s]' % locals())
        cls.storage_classes[name] = storageClass

    @classmethod
    def get(cls, name):
        return cls.storage_classes[name]


class MemStorage(object):
   
    def connect(self):
        pass

    def disconnect(self):
        pass

StorageTypeRegistry.reg('mem', MemStorage)
StorageTypeRegistry.DEFAULT_STORAGE_TYPE = 'mem'


class StorageMixin(ContextMixin):

    @classmethod
    def with_storage(cls, options):
        # Clone a StorageMixin class that contains the options
        return type.__new__('_' + options.get('type',
                                              StorageTypeRegistry.DEFAULT_STORAGE_TYPE) +
                            '_' + cls.__name__,
            [StorageMixin], dict(storage_options=options))

    _storage = None
    storage_options = None

    @property
    def storage(self):
        # gets the storage
        # or will create one if none exists.
        if self._storage is None:
            # Create the project with options set via UbikDB.with_storage(...).
            self.set_storage(self.storage_options)
        assert self._storage is not None
        return self._storage
    @storage.setter
    def storage(self, value):
        self._storage = value
    
    def has_storage(self):
        # a way to check if we have storage, without creating one by default
        return self._storage is not None

    def set_storage(self, options):
        if options is not None:
            assert not self.has_storage(), 'Reconnect is not implemented'
            # create and connect the storage.
            kw = dict(options)
            kw.setdefault('type', StorageTypeRegistry.DEFAULT_STORAGE_TYPE)
            type = options['type']
            del kw['type']
            self.storage = self.StorageTypeRegistry[type](**kw)
            self.storage.connect()
        else:
            if self.has_storage():
                self.storage.disconnect()
                self.storage = None

    @property
    def root(self):
        return db_root

    @property
    def root_key(self):
        return db_root_key

    def traverse_path(self, path):
        return traverse_path(self.root, self.root_key, path)

    def traverse(self, path):
        return traverse(self.root, self.root_key, path)

    def on_get(self, path):
        value = self.traverse(path)
        return [value]

    def on_set(self, path, value):
        print("on_set", path, value)
        traverse = self.traverse_path(path)
        last = traverse[-2]
        last['data'][last['segment']] = value
        # notify listeners
        self.emit_in_context('set', path, value)
