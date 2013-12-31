
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


class TestTraverseGetsetGet(unittest.TestCase, TraverseBase):

    def traverse_get(self, data, path):
        from ..traverse import traverse_getset
        return traverse_getset(data, path)

    def test_null(self):
        self.assertEqual(self.traverse_get(self.data, []), self.data)
        self.assertEqual(self.traverse_get(self.data, ''), self.data)
        self.assertEqual(self.traverse_get(self.data, '/'), self.data)

    def test_simple(self):
        self.assertEqual(self.traverse_get(self.data, 'a'), self.data['a'])
        self.assertEqual(self.traverse_get(self.data, '/a/'), self.data['a'])
        self.assertEqual(self.traverse_get(self.data, 'b'), self.data['b'])
        self.assertEqual(self.traverse_get(self.data, '/a/1'), self.data['a']['1'])

    def test_ignores_dashes(self):
        self.assertEqual(self.traverse_get(self.data, '///'), self.data)
        self.assertEqual(self.traverse_get(self.data, 'a/1'), self.data['a']['1'])
        self.assertEqual(self.traverse_get(self.data, '/a/1/'), self.data['a']['1'])
        self.assertEqual(self.traverse_get(self.data, '///a///1///'), self.data['a']['1'])

    def test_undefined(self):
        self.assertEqual(self.traverse_get(self.data, '/a/1/NO'), None)
        self.assertEqual(self.traverse_get(self.data, '/a/NO'), None)
        self.assertEqual(self.traverse_get(self.data, '/NO'), None)


class TestTraverseGetsetSet(unittest.TestCase, TraverseBase):

    def traverse_set(self, data, path, value):
        from ..traverse import traverse_getset
        return traverse_getset(data, path, value, set=True)

    def test_null(self):
        with self.assertRaises(RuntimeError):
            self.traverse_set(self.data, [], 'X')
        with self.assertRaises(RuntimeError):
            self.traverse_set(self.data, '', 'X')
        with self.assertRaises(RuntimeError):
            self.traverse_set(self.data, '/', 'X')

    def test_simple(self):
        d = self.data
        self.traverse_set(d, 'a', 'X')
        self.assertEqual(d['a'], 'X')
        d = self.data
        self.traverse_set(d, 'a', 'X')
        self.assertEqual(d['a'], 'X')
        d = self.data
        self.traverse_set(d, '/a/', 'X')
        self.assertEqual(d['a'], 'X')
        d = self.data
        self.traverse_set(d, 'b', 'X')
        self.assertEqual(d['b'], 'X')
        d = self.data
        self.traverse_set(d, '/a/1', 'X')
        self.assertEqual(d['a']['1'], 'X')

    def test_ignores_dashes(self):
        with self.assertRaises(RuntimeError):
            self.traverse_set(self.data, '///', 'X')
        d = self.data
        self.traverse_set(d, 'a/1', 'X')
        self.assertEqual(d['a']['1'], 'X')
        d = self.data
        self.traverse_set(d, '/a/1/', 'X')
        self.assertEqual(d['a']['1'], 'X')
        d = self.data
        self.traverse_set(d, '///a///1///', 'X')
        self.assertEqual(d['a']['1'], 'X')

    def test_undefined(self):
        d = self.data
        self.traverse_set(d, '/a/1/NO', 'X')
        self.assertEqual(d['a']['1']['NO'], 'X')
        d = self.data
        self.traverse_set(d, '/a/NO', 'X')
        self.assertEqual(d['a']['NO'], 'X')
        d = self.data
        self.traverse_set(d, '/NO', 'X')
        self.assertEqual(d['NO'], 'X')
        d = self.data
