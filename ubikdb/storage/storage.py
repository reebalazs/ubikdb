
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
    def with_storage(cls, storage_type, **storage_options):
        # Create the storage.
        storage = StorageTypeRegistry.get(storage_type)(**storage_options)
        # Clone a StorageMixin class that contains the
        # storage class as a class attribute.
        return type('_' + storage_type + '_' + cls.__name__, (cls, ), dict(
            storage=storage,
        ))

    storage = None

    def on_watch_context_and_get(self, path, recurse=None):
        """Lets a user watch a context on a specific namespace.

        It also returns the content of the path at this moment
        that can be used as an initial content for later updates.
        This is the same as the result from on_get.
        """
        self.on_watch_context(path, recurse=recurse)
        return self.on_get(path)

    def recv_connect(self):
        assert self.storage is not None, 'UbikDB ought to be applied with_storage'
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
        self.broadcast_in_context('set', path, value)
