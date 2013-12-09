
from __future__ import print_function

from ..context import ContextMixin


class StorageTypeRegistry(object):

    storage_classes = {}

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
    def with_storage(cls, storage_or_storage_type, **storage_options):
        # Create the storage.
        if isinstance(storage_or_storage_type, basestring):
            # If first parameter is a string, create it from the registry, 
            # with provided options.
            storage_type = storage_or_storage_type
            storage = StorageTypeRegistry.get(
                    storage_or_storage_type)(**storage_options)
        else:
            # or just use the provided object
            storage = storage_or_storage_type
            storage_type = storage.__class__.__name__
        # Clone a StorageMixin class that contains the
        # storage class as a class attribute. This makes it sure that
        # the same storage is shared between all instances.
        return type('_' + storage_type + '_' + cls.__name__, (cls, ), dict(
            storage=storage,
        ))

    storage = None

    def recv_connect(self):
        self.storage.connect(self.notify_listeners)

    def recv_disconnect(self):
        self.storage.disconnect(self.notify_listeners)

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
