
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
        # Make sure it is a singleton: there must be only one storage per namespace.
        if self._storage is None:
            # Create the project with options set via UbikDB.with_storage(...).
            self.__class__._storage = self.make_storage(self.storage_type, self.storage_options)
            #StorageMixin._storage = self.make_storage(self.storage_type, self.storage_options)
        assert self._storage is not None
        return self._storage
    
    def make_storage(self, storage_or_storage_type, storage_options=None):
        if isinstance(storage_or_storage_type, basestring):
            # If first parameter is a string, create it from the registry, 
            # with provided options.
            storage = StorageTypeRegistry.get(
                    storage_or_storage_type)(**storage_options)
        else:
            # or just use the provided object
            storage = storage_or_storage_type
        # Connect the storage and set its callback.
        storage.connect(self.notify_listeners)
        return storage

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
