
import unittest

class TestTraversePath(unittest.TestCase):

    def traverse_path(self, data, *path):
        from ..traverse import traverse_path
        return traverse_path(data, *path)

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

    def test_null(self):
        self.assertEqual(self.traverse_path(self.data), [
            {'data': self.data},
        ])
        self.assertEqual(self.traverse_path(self.data, ''), [
            {'data': self.data},
        ])
        self.assertEqual(self.traverse_path(self.data, '/'), [
            {'data': self.data},
        ])

    def test_simple(self):
        self.assertEqual(self.traverse_path(self.data, 'a'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a']},
        ])
        self.assertEqual(self.traverse_path(self.data, '/a/'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a']},
        ])
        self.assertEqual(self.traverse_path(self.data, 'b'), [
            {'data': self.data, 'segment': 'b'},
            {'data': self.data['b']},
        ])
        self.assertEqual(self.traverse_path(self.data, '/a/1'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': '1'},
            {'data': self.data['a']['1']},
        ])

    def test_ignores_dashes(self):
        self.assertEqual(self.traverse_path(self.data, '///'), [
            {'data': self.data},
        ])
        self.assertEqual(self.traverse_path(self.data, 'a/1'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': '1'},
            {'data': self.data['a']['1']},
        ])
        self.assertEqual(self.traverse_path(self.data, '/a/1/'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': '1'},
            {'data': self.data['a']['1']},
        ])
        self.assertEqual(self.traverse_path(self.data, '///a///1///'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': '1'},
            {'data': self.data['a']['1']},
        ])

    def test_undefined(self):
        self.assertEqual(self.traverse_path(self.data, '/a/1/NO'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': '1'},
            {'data': self.data['a']['1'], 'segment': 'NO'},
            {'data': None},
        ])
        self.assertEqual(self.traverse_path(self.data, '/a/NO'), [
            {'data': self.data, 'segment': 'a'},
            {'data': self.data['a'], 'segment': 'NO'},
            {'data': None},
        ])
        self.assertEqual(self.traverse_path(self.data, '/NO'), [
            {'data': self.data, 'segment': 'NO'},
            {'data': None},
        ])
