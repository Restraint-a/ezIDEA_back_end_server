import unittest
from pylint_process import parse_pylint_rate, parse_pylint_output

class TestPylintProcess(unittest.TestCase):

    def test_parse_pylint_rate(self):
        # 测试标准输出格式
        output = "Your code has been rated at 8.00/10 (previous run: 7.50/10, +0.50)"
        expected = [{'当前分数': '8.00', '上次分数': '7.50', '变化': '+0.50'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试没有匹配的情况
        output = "Some text that does not match the pattern"
        self.assertIsNone(parse_pylint_rate(output))

        # 测试不同的评分情况
        output = "Your code has been rated at 9.25/10 (previous run: 9.00/10, +0.25)"
        expected = [{'当前分数': '9.25', '上次分数': '9.00', '变化': '+0.25'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试分数下降的情况
        output = "Your code has been rated at 6.75/10 (previous run: 7.00/10, -0.25)"
        expected = [{'当前分数': '6.75', '上次分数': '7.00', '变化': '-0.25'}]
        self.assertEqual(parse_pylint_rate(output), expected)

        # 测试无变化的情况
        output = "Your code has been rated at 7.00/10 (previous run: 7.00/10, +0.00)"
        expected = [{'当前分数': '7.00', '上次分数': '7.00', '变化': '+0.00'}]
        self.assertEqual(parse_pylint_rate(output), expected)

    def test_parse_pylint_output(self):
        # 测试标准错误输出格式
        output = """\
test.py:2:0: C0304: Final newline missing (missing-final-newline)
another_test.py:5:4: E0602: Undefined variable 'x' (undefined-variable)"""

        expected = [
            {'文件名': 'test.py', '出错行': 2, '出错列': 0, '错误码': 'C0304', '错误信息': 'Final newline missing'},
            {'文件名': 'another_test.py', '出错行': 5, '出错列': 4, '错误码': 'E0602', '错误信息': "Undefined variable 'x'"}
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
            {'文件名': 'test.py', '出错行': 2, '出错列': 0, '错误码': 'C0304', '错误信息': 'Final newline missing'},
            {'文件名': 'test.py', '出错行': 3, '出错列': 0, '错误码': 'E0602', '错误信息': "Undefined variable 'y'"}
        ]
        self.assertEqual(parse_pylint_output(output), expected)

        # 测试空行和注释
        output = """\
# This is a comment line
test.py:2:0: C0304: Final newline missing (missing-final-newline)
another_test.py:5:4: E0602: Undefined variable 'x' (undefined-variable)"""

        expected = [
            {'文件名': 'test.py', '出错行': 2, '出错列': 0, '错误码': 'C0304', '错误信息': 'Final newline missing'},
            {'文件名': 'another_test.py', '出错行': 5, '出错列': 4, '错误码': 'E0602', '错误信息': "Undefined variable 'x'"}
        ]
        self.assertEqual(parse_pylint_output(output), expected)

        # 测试多行错误信息
        output = """\
test.py:2:0: C0304: Final newline missing (missing-final-newline)
another_test.py:5:4: E0602: Undefined variable 'x' (undefined-variable)
yet_another_test.py:10:2: W0603: Using the global statement (global-statement)"""

        expected = [
            {'文件名': 'test.py', '出错行': 2, '出错列': 0, '错误码': 'C0304', '错误信息': 'Final newline missing'},
            {'文件名': 'another_test.py', '出错行': 5, '出错列': 4, '错误码': 'E0602', '错误信息': "Undefined variable 'x'"},
            {'文件名': 'yet_another_test.py', '出错行': 10, '出错列': 2, '错误码': 'W0603', '错误信息': "Using the global statement"}
        ]
        self.assertEqual(parse_pylint_output(output), expected)

if __name__ == '__main__':
    unittest.main()