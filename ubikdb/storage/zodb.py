
from __future__ import print_function

import transaction
from transaction.interfaces import ISynchronizer
from zope.interface import (
    implements,
)

from .storage import StorageTypeRegistry
from ..traverse import (
    traverse_getset,
    split_path,
)


class Synchronizer(object):
    implements(ISynchronizer)

    def __init__(self, storage):
        self.storage = storage

    def beforeCompletion(self, transaction):
        self.storage.before_completion(transaction)

    def afterCompletion(self, transaction):
        pass

    def newTransaction(self, transaction):
        pass


class DefaultMapper(object):

    def __init__(self, root, annotate_attr, annotate_key):
        self.root = root
        self.annotate_attr = annotate_attr
        self.annotate_key = annotate_key

    def traverse_getset(self, path, value=None, set=False):
        if not hasattr(self.root, self.annotate_attr) and set:
            annotation = {}
            setattr(self.root, self.annotate_attr, annotation)
        else:
            annotation = getattr(self.root, self.annotate_attr, {})
        if self.annotate_key not in annotation:
            root = {}
            if set:
                annotation[self.annotate_key] = root
        else:
            root = annotation[self.annotate_key]
        # Now that we have the root, let's traverse it
        # via the normal memory traverser.
        result = traverse_getset(root, path, value, set)
        return result


class ZODBStorage(object):

    def __init__(self, zodb_root, annotate_attr='_ubikdb'):
        self.zodb_root = zodb_root
        self.annotate_attr = annotate_attr
        self.synchronizer = None
        self.notify_changes = None
        self.commit_in_progress = False

    def set_notify_changes(self, callback):
        self.notify_changes = callback

    def connect(self):
        self.synchronizer = Synchronizer(self)
        transaction.manager.registerSynch(self.synchronizer)
        
    def disconnect(self):
        transaction.manager.unregisterSynch(self.synchronizer)
        self.synchronizer = None

    def traverse_getset(self, path, value=None, set=False):
        root = self.zodb_root
        split = split_path(path)
        for i, segment in enumerate(split):
            if segment:
                if segment.startswith('@@'):
                    # all catch forward traverse via specific mapper
                    annotate_key = segment[2:]
                    if annotate_key == '':
                        raise RuntimeError('/@@ properties not yet supported. Use /@@myprop')
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
        value = self.traverse_getset(path)
        return value

    def set(self, path, value):
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
                print('CHANGED', ob, ubikdb_path, ubikdb_value)
                import ipdb; ipdb.set_trace()
                self.notify_changes(ubikdb_path, ubikdb_value)


StorageTypeRegistry.reg('zodb', ZODBStorage)
