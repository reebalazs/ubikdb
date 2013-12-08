
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

    def __init__(self, zodb_root, annotate_attr='_ubikdb'):
        self.zodb_root = zodb_root
        self.annotate_attr = annotate_attr
        self.synchronizer = None
        self._notify_changes = []
        self.commit_in_progress = False

    def connect(self, callback):
        self.synchronizer = Synchronizer(self)
        transaction.manager.registerSynch(self.synchronizer)
        self._notify_changes.append(callback)
        
    def disconnect(self, callback):
        transaction.manager.unregisterSynch(self.synchronizer)
        self.synchronizer = None
        self._notify_changes.remove(callback)

    def notify_changes(self, path, value):
        # The first registered handler is elected to do the job,
        # as it will broadcast to all sockets.
        self._notify_changes[0](path, value)

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
        return self.traverse_getset(path)

    def set(self, path, value):
        self.traverse_getset(path, value, set=True)._p_changed = True
        # Make sure we won't trigger on our own changes.
        self.commit_in_progress = True
        try:
            transaction.commit()
        finally:
            self.commit_in_progress = False

    # XXX This is terrible and just barely works.
    # XXX Need to figure out the correct way for noticing the changes.

    def before_completion(self, transaction):
        if not self.commit_in_progress:
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
        if hasattr(ob, self.annotate_attr):
            annotation = getattr(ob, self.annotate_attr)
            # Just signal everything has changed, for now.
            for key in annotation.keys():
                ubikdb_path = '%s@@%s/' % (path, key)
                ubikdb_value = annotation[key]
                print('CHANGED', self, ubikdb_path, ubikdb_value)
                self.notify_changes(ubikdb_path, ubikdb_value)


StorageTypeRegistry.reg('zodb', ZODBStorage)
