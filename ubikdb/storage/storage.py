
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
        if not self.has_storage():
            # Create the project with options set via UbikDB.with_storage(...).
            self.set_storage(self.storage_type, self.storage_options)
        assert self._storage is not None
        return self._storage
    @storage.setter
    def storage(self, value):
        # Storage is a class method, and it will be shared
        # between multiple sockets using the same storage.
        self.__class__._storage = value
    
    def has_storage(self):
        # a way to check if we have storage, without creating one by default
        return self._storage is not None

    def set_storage(self, storage_or_storage_type, storage_options=None):
        # Disconnect previous storage
        if self.has_storage():
            self.storage.disconnect(self.notify_listeners)
            self.storage = None
        if storage_or_storage_type is not None:
            if isinstance(storage_or_storage_type, basestring):
                # If first parameter is a string, create it from the registry, 
                # with provided options.
                self.storage = StorageTypeRegistry.get(
                        storage_or_storage_type)(**storage_options)
            else:
                self.storage = storage_or_storage_type
            # Connect the storage and set its callback.
            self.storage.connect(self.notify_listeners)
        else:
            if self.has_storage():
                self.storage.disconnect(self.notify_listeners)
                self.storage.set_notify_changes(None)
                self.storage = None

    def on_get(self, path):
        return [self.storage.get(path)]

    def on_set(self, path, value):
        self.storage.set(path, value)
        self.emit_in_context('set', path, value)

    def notify_listeners(self, path, value):
        # the storage will call this
        # but only on the first socket.
        # We broadcast to self too, since we were not
        # the originators.
        self.broadcast_in_context('set', path, value)
