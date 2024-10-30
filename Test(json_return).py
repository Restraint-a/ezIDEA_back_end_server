import unittest
from unittest.mock import patch
from json_return import allowed_file, handle_uploaded_file, process

class TestJsonReturn(unittest.TestCase):

    def test_allowed_file(self):
        self.assertTrue(allowed_file('test.py'))
        self.assertFalse(allowed_file('test.txt'))

    @patch('json_return.process_file_out')
    @patch('json_return.process_report')
    def test_handle_uploaded_file(self, mock_process_report, mock_process_file_out):
        mock_process_report.return_value = 'test_result.json'
        result = handle_uploaded_file('test.py')
        self.assertEqual(result, 'test_result.json')

    @patch('json_return.os.path.exists')
    @patch('json_return.handle_uploaded_file')
    def test_process(self, mock_handle_uploaded_file, mock_exists):
        mock_exists.return_value = True
        mock_handle_uploaded_file.return_value = 'test_result.json'
        process('test.py')
        mock_handle_uploaded_file.assert_called_once_with('test.py')

if __name__ == '__main__':
    unittest.main()