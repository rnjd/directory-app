import os
import unittest
from unittest.mock import patch
from src import api

root = '/root/'


class TestApi(unittest.TestCase):

    def test_get_contents_endpoint(self):
        api.app.config['TESTING'] = True

        with api.app.test_client() as client:
            with patch.object(api, 'get_contents', return_value=['a', 'b']) as get_contents_mock:
                result = client.get('/')
                get_contents_mock.assert_called_once()
                self.assertEqual(result.data, b'["a","b"]\n')
                self.assertEqual(result.status, '200 OK')


class TestGetContents(unittest.TestCase):
    def test_path_exists_error(self):
        with patch.object(os.path, 'exists', return_value=False) as path_mock:
            with self.assertRaises(ValueError):
                api.get_contents(root)
                path_mock.assert_called_once_with(root)

    def test_list_dir_for_directory(self):
        returned_contents = ['a', 'b', 'c']

        with patch.object(os.path, 'exists', return_value=True) as path_mock:
            with patch.object(os.path, 'isfile', return_value=False) as isfile_mock:
                with patch.object(os, 'listdir', return_value=['hello', 'world.txt']) as listdir_mock:
                    with patch.object(api, '__get_content_details', return_value=returned_contents) as content_mock:
                        result = api.get_contents(root)

                        path_mock.assert_called_once_with(root)
                        isfile_mock.assert_called_once_with(root)
                        listdir_mock.assert_called_once_with(root)
                        content_mock.assert_called_with('/root/world.txt')
                        self.assertEqual(result, ['["a", "b", "c"]', '["a", "b", "c"]'])
