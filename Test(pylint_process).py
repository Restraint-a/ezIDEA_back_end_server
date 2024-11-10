from pylint_process import parse_pylint_rate, parse_pylint_output

import unittest

class TestPylintParsing(unittest.TestCase):

    def test_parse_pylint_rate(self):
        # 测试标准输出格式
        output = "Your code has been rated at 8.00/10 (previous run: 7.50/10, +0.50)"
        expected = [{'current_score': '8.00', 'previous_score': '7.50', 'change': '+0.50'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试没有匹配的情况
        output = "Some text that does not match the pattern"
        self.assertIsNone(parse_pylint_rate(output))

        # 测试不同的评分情况
        output = "Your code has been rated at 9.25/10 (previous run: 9.00/10, +0.25)"
        expected = [{'current_score': '9.25', 'previous_score': '9.00', 'change': '+0.25'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试分数下降的情况
        output = "Your code has been rated at 6.75/10 (previous run: 7.00/10, -0.25)"
        expected = [{'current_score': '6.75', 'previous_score': '7.00', 'change': '-0.25'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试无变化的情况
        output = "Your code has been rated at 7.00/10 (previous run: 7.00/10, +0.00)"
        expected = [{'current_score': '7.00', 'previous_score': '7.00', 'change': '+0.00'}]
        self.assertEqual(parse_pylint_rate(output), expected)

    def test_parse_pylint_output(self):
        # 测试标准错误输出格式
        output = """\
test.py:2:0: C0304: Final newline missing (missing-final-newline)
another_test.py:5:4: E0602: Undefined variable 'x' (undefined-variable)"""

        expected = [
            {'file_name': 'another_test.py', 'error_line': 5, 'error_col': 4, 'error_code': 'E0602', 'error_message': "Undefined variable 'x'"},
        ]
        self.assertEqual(parse_pylint_output(output), expected)

        # 测试没有匹配的情况
        output = "Some text that does not match the pattern"
        self.assertEqual(parse_pylint_output(output), [])

        # 测试多个错误在同一文件中
        output = """\
test.py:2:0: C0304: Final newline missing (missing-final-newline)
test.py:3:0: E0602: Undefined variable 'y' (undefined-variable)"""

        expected = [
            {'file_name': 'test.py', 'error_line': 3, 'error_col': 0, 'error_code': 'E0602', 'error_message': "Undefined variable 'y'"}
        ]
        self.assertEqual(parse_pylint_output(output), expected)

        # 测试多行错误信息
        output = """\
test.py:2:0: C0304: Final newline missing (missing-final-newline)
another_test.py:5:4: E0602: Undefined variable 'x' (undefined-variable)
yet_another_test.py:10:2: W0603: Using the global statement (global-statement)"""

        expected = [
            {'file_name': 'another_test.py', 'error_line': 5, 'error_col': 4, 'error_code': 'E0602', 'error_message': "Undefined variable 'x'"},
            {'file_name': 'yet_another_test.py', 'error_line': 10, 'error_col': 2, 'error_code': 'W0603', 'error_message': "Using the global statement"}
        ]
        self.assertEqual(parse_pylint_output(output), expected)

if __name__ == '__main__':
    unittest.main()
