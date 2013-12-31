
from __future__ import print_function

import transaction

from ..storage import StorageTypeRegistry
from ...traverse import split_path
from .synchronizer import Synchronizer
from .mapper import (
    DefaultMapper,
    AttributeMapper,
)


class ZODBStorage(object):

    # primitive semaphore
    commit_in_progress = 0

    def __init__(self, zodb_root, annotate_attr='_ubikdb'):
        self.zodb_root = zodb_root
        self.annotate_attr = annotate_attr
        self._notify_changes = None
        self.synchronizer = Synchronizer()

    def connect(self, callback):
        self._notify_changes = callback
        self.synchronizer.on(self.before_completion)
        
    def disconnect(self, callback):
        self._notify_changes = None
        self.synchronizer.off(self.before_completion)

    def notify_changes(self, path, value):
        if self._notify_changes is not None:
            self._notify_changes(path, value)

    def traverse_getset(self, path, value=None, set=False):
        root = self.zodb_root
        split = split_path(path)
        for i, segment in enumerate(split):
            if segment:
                if segment.startswith('@@'):
                    # all catch forward traverse via specific mapper
                    annotate_key = segment[2:]
                    if annotate_key == '':
                        mapper = AttributeMapper(root)
                    else:
                        mapper = DefaultMapper(root, self.annotate_attr, annotate_key)
                    result = mapper.traverse_getset(split[i+1:], value, set)
                    if set:
                        # return this object, instead, for setting it dirty
                        return root
                    else:
                        return result
                else:
                    # normal traverse through ZODB content
                    annotate_key = None
                    root = root.get(segment, None)
                    if root is None:
                        if set:
                            raise RuntimeError('Readonly. Setting before /@@ is not implemented. 1[%s]' % (path, ))
                        # Not found
                        return None
        if set:
            raise RuntimeError('Readonly. Setting before /@@ is not implemented. 2[%s]' % (path, ))
        return root

    def get(self, path):
        transaction.abort()
        try:
            return self.traverse_getset(path)
        finally:
            transaction.abort()

    def set(self, path, value):
        transaction.abort()
        self.traverse_getset(path, value, set=True)._p_changed = True
        # Make sure we won't trigger on our own changes.
        ZODBStorage.commit_in_progress += 1
        try:
            transaction.commit()
        finally:
            ZODBStorage.commit_in_progress -= 1

    # XXX This is terrible and just barely works.
    # XXX Need to figure out the correct way for noticing the changes.

    def before_completion(self, transaction):
        if ZODBStorage.commit_in_progress == 0:
            for res in transaction._resources:
                if hasattr(res, 'connections'):
                    conn = res.connections['']
                    objs = conn._registered_objects
                    self.on_zodb_transaction(objs)
                    break

    def on_zodb_transaction(self, objs):
        for ob in objs:
            # TODO checking interface is needed here.
            oid = getattr(ob, '__oid__', None)
            if oid is not None:
                path = self.get_zodb_path(ob)
                self.on_zodb_changed(path, ob)

    def get_zodb_path(self, ob):
        parent = ob.__parent__
        if parent == None:
            return '/'
        else:
            return self.get_zodb_path(parent) + ob.__name__ + '/'

    def on_zodb_changed(self, path, ob):
        # signal changes in the annotation
        if hasattr(ob, self.annotate_attr):
            annotation = getattr(ob, self.annotate_attr)
            # Just signal everything has changed, for now.
            for key in annotation.keys():
                notify_path = '%s@@%s/' % (path, key)
                value = annotation[key]
                self.notify_changes(notify_path, value)
        # signal property changes on the context itself
        value = AttributeMapper(ob).traverse_getset('')
        self.notify_changes(path + '@@/', value)


StorageTypeRegistry.reg('zodb', ZODBStorage)
