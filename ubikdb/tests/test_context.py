
import unittest


class TestContextMixin(unittest.TestCase):

    def inst(self):
        from socketio.namespace import BaseNamespace
        from ..context import ContextMixin
        class TestNamespace(BaseNamespace, ContextMixin):
            pass
        environ = dict(
            socketio=MockSocket(),
        )
        ns_name = 'testns'
        request = None
        return TestNamespace(environ, ns_name, request=request)

    def store(self, inst, **kw):
        store = inst.session \
            .setdefault('context_mixin', {}) \
            .setdefault(inst.ns_name, MockEventRegistry())
        store.__dict__.update(kw)
        return store

    def test_creating(self):
        inst = self.inst()
        self.assert_(inst)

    def test_on_watch_context(self):
        inst = self.inst()
        self.assert_('context_mixin' not in inst.session)
        inst.on_watch_context('/foo/bar')
        store = self.store(inst)
        self.assertEqual(store.target,
            set(['/foo/bar']),
        )
        self.assertEqual(store.parent,
            set([]),
        )
        inst.on_watch_context('/blah')
        self.assertEqual(store.target,
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(store.parent,
            set([]),
        )
        inst.on_watch_context('/foo/boo', recurse={'parent': True})
        self.assertEqual(store.target,
            set(['/foo/bar', '/blah', '/foo/boo']),
        )
        self.assertEqual(store.parent,
            set(['/foo/boo']),
        )
        inst.on_watch_context('/foo/bar', recurse={'parent': True})
        self.assertEqual(store.target,
            set(['/foo/bar', '/blah', '/foo/boo']),
        )
        self.assertEqual(store.parent,
            set(['/foo/boo', '/foo/bar']),
        )

    def test_on_unwatch_context(self):
        inst = self.inst()
        store = self.store(inst,
            target=set(['/foo/bar', '/blah', '/foo/boo']),
            parent=set(['/foo/boo', '/foo/bar']),
        )
        inst.on_unwatch_context('/foo/bar')
        self.assertEqual(store.target,
            set(['/blah', '/foo/boo']),
        )
        self.assertEqual(store.parent,
            set(['/foo/boo']),
        )
        inst.on_unwatch_context('/foo/boo')
        self.assertEqual(store.target,
            set(['/blah']),
        )
        self.assertEqual(store.parent,
            set([]),
        )
        inst.on_unwatch_context('/blah')
        self.assertEqual(store.target,
            set([]),
        )
        self.assertEqual(store.parent,
            set([]),
        )

    def test_on_unwatch_context_miss(self):
        inst = self.inst()
        inst.on_unwatch_context('/NO/SUCH')
        store = self.store(inst)
        self.assertEqual(store.target,
            set([]),
        )
        self.assertEqual(store.parent,
            set([]),
        )

    def test_on_watch_context_children(self):
        inst = self.inst()
        self.assert_('context_mixin' not in inst.session)
        inst.on_watch_context('/foo/bar')
        inst.on_watch_context('/foo/burr', recurse={'parent': True})
        store = self.store(inst)
        self.assertEqual(store.children,
            set([]),
        )

    #def test_emit_in_context(self):
    #    inst = self.inst()


class MockSocket(object):
    def __init__(self):
        self.session = dict()


class MockEventRegistry(object):

    def __init__(self):
        self.target = set()
        self.parent = set()
        self.children = set()
