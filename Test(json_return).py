import unittest
from pylint_process import process_file_out, process_report
import os
import json
import tempfile

class TestPylintFileProcessing(unittest.TestCase):

    def setUp(self):
        # 创建一个临时目录用于存放测试文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_filename = os.path.join(self.temp_dir.name, 'test.py')
        with open(self.test_filename, 'w') as f:
            f.write('def foo():\n    print("Hello, World!")')

    def tearDown(self):
        # 清理临时目录
        self.temp_dir.cleanup()

    def test_process_file_out(self):
        # 生成报告文件
        process_file_out(self.test_filename)

        # 确认报告文件已生成
        report_filename = f"{os.path.splitext(self.test_filename)[0]}_report.txt"
        self.assertTrue(os.path.exists(report_filename))

    def test_process_report(self):
        # 先生成报告文件
        process_file_out(self.test_filename)

        # 处理报告并生成 JSON 文件
        result_filename = process_report(self.test_filename)

        # 确认 JSON 文件已生成
        self.assertTrue(os.path.exists(result_filename))

        # 读取 JSON 文件并验证其内容
        with open(result_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIn('错误信息', data)
            self.assertIn('评分情况', data)

if __name__ == '__main__':
    unittest.main()