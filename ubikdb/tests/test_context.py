
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

class MockSocket(object):
    def __init__(self):
        self.session = dict()