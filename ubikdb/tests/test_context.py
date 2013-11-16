
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

    def test_creating(self):
        inst = self.inst()
        self.assert_(inst)

    def test_on_watch_context(self):
        inst = self.inst()
        self.assertEqual(inst.session['contexts']['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )
        inst.on_watch_context('/foo/bar')
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/foo/bar']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )
        inst.on_watch_context('/blah')
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )
        inst.on_watch_context('/foo/boo', recurse={'parent': True})
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/foo/bar', '/blah', '/foo/boo']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set(['/foo/boo']),
        )
        inst.on_watch_context('/foo/bar', recurse={'parent': True})
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/foo/bar', '/blah', '/foo/boo']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set(['/foo/boo', '/foo/bar']),
        )

    def test_on_unwatch_context(self):
        inst = self.inst()
        inst.session['contexts']['testns'] = \
            set(['/foo/bar', '/blah', '/foo/boo'])
        inst.session['contexts_parent']['testns'] = \
            set(['/foo/boo', '/foo/bar'])
        inst.on_unwatch_context('/foo/bar')
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/blah', '/foo/boo']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set(['/foo/boo']),
        )
        inst.on_unwatch_context('/foo/boo')
        self.assertEqual(inst.session['contexts']['testns'],
            set(['/blah']),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )
        inst.on_unwatch_context('/blah')
        self.assertEqual(inst.session['contexts']['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )

    def test_on_unwatch_context_miss(self):
        inst = self.inst()
        inst.on_unwatch_context('/NO/SUCH')
        self.assertEqual(inst.session['contexts']['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )

    def test_on_watch_context_children(self):
        inst = self.inst()
        self.assertEqual(inst.session['contexts']['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts_parent']['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts_children']['testns'],
            set([]),
        )
        inst.on_watch_context('/foo/bar')
        inst.on_watch_context('/foo/burr', recurse={'parent': True})
        self.assertEqual(inst.session['contexts_children']['testns'],
            set([]),
        )

    #def test_emit_in_context(self):
    #    inst = self.inst()


class MockSocket(object):
    def __init__(self):
        self.session = dict()