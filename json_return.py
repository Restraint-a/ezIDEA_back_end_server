import os
from pylint_process import process_file_out, process_report

# 定义处理文件保存目录
PROCESS_FOLDER = 'processes'
# 如果目录不存在，则创建
if not os.path.exists(PROCESS_FOLDER):
    os.makedirs(PROCESS_FOLDER)

def allowed_file(filename):
    """
    检查文件类型是否允许
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'py'


def handle_uploaded_file(file_path):
    """
    处理上传的文件，并生成报告

    参数：
    - file_path (str): 文件的路径

    返回：
    - result_filename (str): 处理后生成的 JSON 文件的名称
    """
    if allowed_file(file_path):
        process_file_out(file_path)
        result_filename = process_report(file_path)
        #print(result_filename)
        return result_filename
    else:
        raise ValueError("File type not allowed")


def process(file_name):
    """
    主处理函数，用于处理单个文件

    参数：
    - file_name (str): 要处理的文件名称
    """
    if not os.path.exists(file_name):
        print("File not found.")
        return

    try:
        result_filename = handle_uploaded_file(file_name)
        print(f"Processed file: {result_filename}")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    file_name = 'test.py'

    # 示例文件路径
    file_name = os.path.join(PROCESS_FOLDER, file_name)
    process(file_name)
