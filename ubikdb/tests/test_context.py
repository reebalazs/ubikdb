
import unittest
import mock

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
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )
        inst.on_watch_context('/foo/bar', recurse=False)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )
        inst.on_watch_context('/blah', recurse=False)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )
        inst.on_watch_context('/foo/boo', recurse=True)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set(['/foo/boo']),
        )
        inst.on_watch_context('/foo/bar', recurse=True)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set(['/foo/boo', '/foo/bar']),
        )

    def test_on_unwatch_context(self):
        inst = self.inst()
        inst.session['contexts'][False]['testns'] = \
            set(['/foo/bar', '/blah'])
        inst.session['contexts'][True]['testns'] = \
            set(['/foo/boo', '/foo/bar'])
        inst.on_unwatch_context('/foo/bar', recurse=True)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set(['/foo/boo']),
        )
        inst.on_unwatch_context('/foo/boo', recurse=True)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar', '/blah']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )
        inst.on_unwatch_context('/blah', recurse=False)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set(['/foo/bar']),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )
        inst.on_unwatch_context('/foo/bar', recurse=False)
        self.assertEqual(inst.session['contexts'][False]['testns'],
            set([]),
        )
        self.assertEqual(inst.session['contexts'][True]['testns'],
            set([]),
        )

    def test_on_unwatch_context_miss(self):
        inst = self.inst()
        self.assertRaisesRegexp(KeyError, "^'/NO/SUCH'$",
            inst.on_unwatch_context, '/NO/SUCH', recurse=False)
        self.assertRaisesRegexp(KeyError, "^'/NO/SUCH'$",
            inst.on_unwatch_context, '/NO/SUCH', recurse=True)

    def test_emit_in_context(self):
        inst = self.inst()


class MockSocket(object):
    def __init__(self):
        self.session = dict()