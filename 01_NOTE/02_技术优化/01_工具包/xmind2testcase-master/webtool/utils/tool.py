import zipfile
import json

import openpyxl
import pandas as pd
import os
import shutil
from typing import List, Dict
from datetime import datetime


def save_json_to_file(data, file_path: str):
    """
    将JSON数据保存到文件
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # 清除目录内容，防止占内存
        check_and_clean_directory(os.path.dirname(file_path))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"JSON数据已保存到: {file_path}")
        return True
    except Exception as e:
        print(f"保存JSON数据时出错: {e}")
        return False


def extract_xmind_content(xmind_path: str, output_dir: str = None) -> List[Dict]:
    """
    从XMind文件中提取主题数据，返回字典列表
    """
    # 创建临时解压目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extract_dir = f'/tmp/xmind_extract_{timestamp}'

    # 确保目录存在
    os.makedirs(extract_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(xmind_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # 尝试查找content.json（XMind 8及以上版本）
        content_json_path = os.path.join(extract_dir, 'content.json')

        if not os.path.exists(content_json_path):
            # 尝试其他可能的路径
            content_json_path = os.path.join(extract_dir, 'content', 'content.json')
            if not os.path.exists(content_json_path):
                raise FileNotFoundError("未找到content.json，可能不是新版XMind文件")

        with open(content_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 保存原始JSON数据到文件（如果指定了输出目录）
        if output_dir:
            original_json_path = os.path.join(output_dir, f"xmind_original_{timestamp}.json")
            save_json_to_file(data, original_json_path)

        # 调试：打印数据结构
        print(f"数据类型: {type(data)}")
        if isinstance(data, list) and len(data) > 0:
            print(f"列表长度: {len(data)}")
            print(f"列表第一个元素类型: {type(data[0])}")
            if isinstance(data[0], dict):
                print(f"列表第一个元素的键: {list(data[0].keys())}")

        # 根据实际数据结构调整解析逻辑
        all_test_cases = []

        # 如果data是列表，则每个元素代表一个工作表(sheet)
        if isinstance(data, list):
            for i, sheet in enumerate(data):
                print(f"正在处理第 {i + 1} 个工作表")

                # 尝试不同的可能键名
                root_topic = None
                if isinstance(sheet, dict):
                    root_topic = sheet.get('rootTopic') or sheet.get('RootTopic') or sheet.get('topic') or {}
                    print(
                        f"工作表 {i + 1} 的根主题键: {list(root_topic.keys()) if isinstance(root_topic, dict) else '不是字典'}")
                else:
                    print(f"工作表 {i + 1} 不是字典类型: {type(sheet)}")
                    continue

                # 解析测试用例
                test_cases = _parse_test_cases(root_topic, f"工作表{i + 1}")
                all_test_cases.extend(test_cases)
        # 如果data是字典，则尝试获取sheets键
        elif isinstance(data, dict):
            sheets = data.get('sheets', [])
            for i, sheet in enumerate(sheets):
                root_topic = sheet.get('rootTopic', {})
                test_cases = _parse_test_cases(root_topic, f"工作表{i + 1}")
                all_test_cases.extend(test_cases)

        # 保存解析后的测试用例数据到JSON文件（如果指定了输出目录）
        if output_dir and all_test_cases:
            parsed_json_path = os.path.join(output_dir, f"xmind_parsed_{timestamp}.json")
            save_json_to_file(all_test_cases, parsed_json_path)

        return all_test_cases

    finally:
        # 清理临时目录
        try:
            shutil.rmtree(extract_dir)
            print(f"已清理临时目录: {extract_dir}")
        except Exception as e:
            print(f"清理临时目录时出错: {e}")


def _parse_test_cases(root_topic: Dict, sheet_name: str) -> List[Dict]:
    """
    解析测试用例，返回结构化的测试用例列表
    """
    if not root_topic or not isinstance(root_topic, dict):
        return []

    test_cases = []

    # 获取模块（根主题的子主题）
    modules = _get_children(root_topic)

    for module_idx, module in enumerate(modules):
        module_title = module.get('title') or module.get('Title') or module.get('label') or f"模块{module_idx + 1}"

        # 获取测试用例（模块的子主题）
        cases = _get_children(module)

        for case_idx, case in enumerate(cases):
            case_title = case.get('title') or case.get('Title') or case.get('label') or f"测试用例{case_idx + 1}"

            # 获取步骤和预期（测试用例的子主题）
            steps_and_expectations = _get_children(case)

            # 处理步骤和预期
            steps_text = ""
            expectations_text = ""

            for step_idx, step in enumerate(steps_and_expectations):
                step_title = step.get('title') or step.get('Title') or step.get('label') or f"步骤{step_idx + 1}"

                # 获取预期（步骤的子主题）
                expectations = _get_children(step)

                # 格式化步骤文本
                steps_text += f"{step_idx + 1}. {step_title}\n"

                # 格式化预期文本
                if expectations:
                    for exp_idx, exp in enumerate(expectations):
                        exp_title = exp.get('title') or exp.get('Title') or exp.get('label') or f"预期{exp_idx + 1}"
                        expectations_text += f"{step_idx + 1}. {exp_title}\n"
                else:
                    expectations_text += f"{step_idx + 1}. \n"

            # 移除最后的换行符
            if steps_text:
                steps_text = steps_text.strip()
            if expectations_text:
                expectations_text = expectations_text.strip()

            # 创建测试用例
            test_case = {
                '模块': module_title,
                '测试用例': case_title,
                '步骤': steps_text,
                '预期': expectations_text,
                '工作表': sheet_name
            }
            test_cases.append(test_case)

    return test_cases


def _get_children(topic: Dict) -> List[Dict]:
    """
    获取主题的子主题列表
    """
    if not topic or not isinstance(topic, dict):
        return []

    # 尝试不同的可能键名
    children = topic.get('children') or topic.get('Children') or topic.get('topics') or {}

    # 处理不同的子主题结构
    if isinstance(children, list):
        return children
    elif isinstance(children, dict):
        # 尝试获取附加的子主题
        attached = children.get('attached') or children.get('Attached') or children.get('topics') or []
        if isinstance(attached, list):
            return attached

    return []


def save_to_excel(data: List[Dict], output_path: str):
    """
    将数据保存为Excel文件，按照指定格式
    """
    if not data:
        print("没有提取到数据，无法创建Excel文件")
        return

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 重新排列列的顺序
    column_order = ['工作表', '模块', '测试用例', '步骤', '预期']
    df = df.reindex(columns=column_order)

    # 尝试使用openpyxl，如果失败则使用默认引擎
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 按工作表分组
            if '工作表' in df.columns:
                for sheet_name, group in df.groupby('工作表'):
                    # 移除工作表列
                    group = group.drop('工作表', axis=1)
                    group.to_excel(writer, sheet_name=sheet_name, index=False)

                    # 获取工作表对象以设置列宽
                    worksheet = writer.sheets[sheet_name]
                    # 设置列宽
                    worksheet.column_dimensions['A'].width = 20  # 模块
                    worksheet.column_dimensions['B'].width = 30  # 测试用例
                    worksheet.column_dimensions['C'].width = 50  # 步骤
                    worksheet.column_dimensions['D'].width = 50  # 预期

                    # 设置单元格自动换行
                    for row in worksheet.iter_rows():
                        for cell in row:
                            cell.alignment = openpyxl.styles.Alignment(wrap_text=True)
            else:
                df.to_excel(writer, index=False)
    except ImportError:
        print("openpyxl未安装，尝试使用默认引擎")
        df.to_excel(output_path, index=False)

    print(f"成功提取 {len(data)} 个测试用例")


def convert_xmind_to_excel(xmind_path: str, excel_path: str, json_output_dir: str = None):
    """
    将XMind文件转换为Excel文件，并可选择保存JSON数据
    """
    try:
        # 提取XMind内容
        test_cases = extract_xmind_content(xmind_path, json_output_dir)

        if test_cases:
            # 保存到Excel
            save_to_excel(test_cases, excel_path)
            print(f"转换完成！Excel文件已保存至：{excel_path}")

            # 如果指定了JSON输出目录，也保存解析后的数据
            if json_output_dir:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_json_path = os.path.join(json_output_dir, f"xmind_final_{timestamp}.json")
                save_json_to_file(test_cases, final_json_path)
        else:
            print("未提取到任何测试用例数据，请检查XMind文件格式")

    except Exception as e:
        print(f"转换过程中出错: {e}")
        import traceback
        traceback.print_exc()
        print("建议检查XMind文件格式或尝试使用其他方法")
    return excel_path


def check_and_clean_directory(directory_path, size_limit_mb=1):
    """
    检查目录大小，如果超过限制则删除目录下的所有文件

    Args:
        directory_path (str): 要检查的目录路径
        size_limit_mb (int): 大小限制，单位MB，默认为1MB
    """
    # 计算目录总大小
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except OSError:
                # 处理无法访问的文件
                continue

    # 转换为MB
    total_size_mb = total_size / (1024 * 1024)

    # 检查是否超过限制
    if total_size_mb > size_limit_mb:
        print(f"目录大小 {total_size_mb:.2f} MB 超过限制 {size_limit_mb} MB，开始清理...")

        # 删除目录下的所有文件（保留子目录结构）
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    os.remove(filepath)
                    print(f"已删除文件: {filepath}")
                except OSError as e:
                    print(f"删除文件失败 {filepath}: {e}")

        print("清理完成")
    else:
        print(f"目录大小 {total_size_mb:.2f} MB 未超过限制 {size_limit_mb} MB，无需清理")

def run_convert_xmind_to_excel(xmind_file: str, excel_file: str, json_output_dir: str):
    excel_file,json_output_dir = "./excel","./json"
    convert_xmind_to_excel(xmind_file, excel_file, json_output_dir)
