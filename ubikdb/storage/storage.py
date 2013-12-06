
from __future__ import print_function

from ..context import ContextMixin


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


class StorageMixin(ContextMixin):

    @classmethod
    def with_storage(cls, storage_type, **storage_options):
        # Clone a StorageMixin class that contains the options
        return type('_' + storage_type +
                            '_' + cls.__name__,
            (cls, ), dict(
                storage_type=storage_type,
                storage_options=storage_options,
                ))

    _storage = None
    storage_type = StorageTypeRegistry.DEFAULT_STORAGE_TYPE
    storage_options = None

    @property
    def storage(self):
        # gets the storage
        # or will create one if none exists.
        if self._storage is None:
            # Create the project with options set via UbikDB.with_storage(...).
            self.set_storage(self.storage_type, self.storage_options)
        assert self._storage is not None
        return self._storage
    @storage.setter
    def storage(self, value):
        self._storage = value
    
    def has_storage(self):
        # a way to check if we have storage, without creating one by default
        return self._storage is not None

    def set_storage(self, storage_type, storage_options):
        if storage_type is not None:
            assert not self.has_storage(), 'Reconnect is not implemented'
            # create and connect the storage.
            self.storage = StorageTypeRegistry.get(storage_type)(**storage_options)
            self.storage.connect()
        else:
            if self.has_storage():
                self.storage.disconnect()
                self.storage = None

    def on_get(self, path):
        return self.storage.get(path)

    def on_set(self, path, value):
        self.storage.set(path, value)
        # notify listeners
        self.emit_in_context('set', path, value)
