
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
        self.assertEqual(inst.session['contexts'], set([
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))
        inst.on_watch_context('/foo/bar', recurse=False)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))
        inst.on_watch_context('/blah', recurse=False)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar', 'testns:/blah',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))
        inst.on_watch_context('/foo/boo', recurse=True)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar', 'testns:/blah',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
            'testns:/foo/boo',
        ]))
        inst.on_watch_context('/foo/bar', recurse=True)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar', 'testns:/blah',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
            'testns:/foo/boo', 'testns:/foo/bar'
        ]))

    def test_on_unwatch_context(self):
        inst = self.inst()
        inst.session['contexts'] = set([
            'testns:/foo/bar', 'testns:/blah',
        ])
        inst.session['contexts_recurse'] = set([
            'testns:/foo/boo', 'testns:/foo/bar'
        ])
        inst.on_unwatch_context('/foo/bar', recurse=True)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar', 'testns:/blah',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
            'testns:/foo/boo',
        ]))
        inst.on_unwatch_context('/foo/boo', recurse=True)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar', 'testns:/blah',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))
        inst.on_unwatch_context('/blah', recurse=False)
        self.assertEqual(inst.session['contexts'], set([
            'testns:/foo/bar',
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))
        inst.on_unwatch_context('/foo/bar', recurse=False)
        self.assertEqual(inst.session['contexts'], set([
        ]))
        self.assertEqual(inst.session['contexts_recurse'], set([
        ]))

    def test_on_unwatch_context_miss(self):
        inst = self.inst()
        self.assertRaisesRegexp(KeyError, "^'testns:/NO/SUCH'$",
            inst.on_unwatch_context, '/NO/SUCH', recurse=False)
        self.assertRaisesRegexp(KeyError, "^'testns:/NO/SUCH'$",
            inst.on_unwatch_context, '/NO/SUCH', recurse=True)


class MockSocket(object):
    def __init__(self):
        self.session = dict()