import unittest
import os
from tempfile import NamedTemporaryFile
from json import dumps, load
from improve_code import *

class TestCodeImprovement(unittest.TestCase):

    def setUp(self):
        # 创建一个临时文件，模拟真实的JSON文件
        self.temp_file = NamedTemporaryFile(mode='w+', delete=False, suffix='_result.json')
        self.temp_file.write(dumps({
            "Error(s)": [
                {"error_message": "Undefined variable '__main__'", "error_line": 5},
                {"error_message": "Syntax error", "error_line": 10}
            ]
        }))
        self.temp_file.close()
        self.output_file = None

    def tearDown(self):
        # 清理临时文件
        os.remove(self.temp_file.name)
        if self.output_file and os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_read_result(self):
        data = read_result(self.temp_file.name)
        self.assertIsInstance(data, dict)
        self.assertIn('Error(s)', data)

    def test_is_want(self):
        self.assertEqual(is_want({"error_message": "Undefined variable '__main__'"}), 0)
        self.assertEqual(is_want({"error_message": "Syntax error"}), -1)

    def test_improve(self):
        result = read_result(self.temp_file.name)
        with NamedTemporaryFile(delete=False, suffix='_improved.json') as output_file:
            self.output_file = output_file.name
            improve(result, self.output_file)
        with open(self.output_file, 'r') as f:
            improved_data = load(f)
        self.assertIn('improved_items', improved_data)


if __name__ == '__main__':
    unittest.main()