
import unittest
import mock

class TraverseBase(object):

    @property
    def data(self):
        return {
            'a': {
                '1': 'a-one',
                '2': 'a-two',
            },
            'b': {
                '1': 'b-one',
                '2': 'b-two',
            },

        }

class TestTraverseGetset(unittest.TestCase, TraverseBase):

    def traverse_getset(self, data, *path):
        from ..traverse import traverse_getset
        return traverse_getset(data, *path)

    def test_null(self):
        self.assertEqual(self.traverse_getset(self.data, []), self.data)
        self.assertEqual(self.traverse_getset(self.data, ''), self.data)
        self.assertEqual(self.traverse_getset(self.data, '/'), self.data)

    def test_simple(self):
        self.assertEqual(self.traverse_getset(self.data, 'a'), self.data['a'])
        self.assertEqual(self.traverse_getset(self.data, '/a/'), self.data['a'])
        self.assertEqual(self.traverse_getset(self.data, 'b'), self.data['b'])
        self.assertEqual(self.traverse_getset(self.data, '/a/1'), self.data['a']['1'])

    def test_ignores_dashes(self):
        self.assertEqual(self.traverse_getset(self.data, '///'), self.data)
        self.assertEqual(self.traverse_getset(self.data, 'a/1'), self.data['a']['1'])
        self.assertEqual(self.traverse_getset(self.data, '/a/1/'), self.data['a']['1'])
        self.assertEqual(self.traverse_getset(self.data, '///a///1///'), self.data['a']['1'])

    def test_undefined(self):
        self.assertEqual(self.traverse_getset(self.data, '/a/1/NO'), None)
        self.assertEqual(self.traverse_getset(self.data, '/a/NO'), None)
        self.assertEqual(self.traverse_getset(self.data, '/NO'), None)
