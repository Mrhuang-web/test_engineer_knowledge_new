import pandas as pd
from xmindparser import xmind_to_dict
import argparse
import os


def xmind_to_excel(xmind_file, excel_file):
    """
    将XMind文件转换为Excel格式
    结构: 中心主题 -> 模块 -> 用例 -> 前置条件、操作步骤、预期结果
    """
    try:
        # 解析XMind文件
        data = xmind_to_dict(xmind_file)

        # 保存json
        jsonname = xmind_file.split('\\')[-1].split('.')[0]
        to_json = str(data).replace("'", '"')
        with open(f'./JsonDoc/{jsonname}.json', 'w', encoding='utf-8') as f:
            f.write(to_json)

        # 提取中心主题
        central_topic = data[0]['topic']

        # 准备Excel数据
        excel_data = []

        # 遍历模块
        for module in central_topic['topics']:
            module_name = module['title']

            # 遍历用例
            for use_case in module['topics']:
                use_case_name = use_case['title']

                # 初始化前置条件、操作步骤和预期结果
                preconditions = ""
                steps = ""
                expected_result = ""

                # 遍历用例的详细信息
                for detail in use_case['topics']:
                    detail_title = detail['title']

                    if '前置条件' in detail_title:
                        preconditions = detail_title.split('：', 1)[1].strip().replace('、', '.').replace('；',
                                                                                                        '\n') if '：' in detail_title else ""
                    elif '操作步骤' in detail_title:
                        steps = detail_title.split('：', 1)[1].strip().replace('、', '.').replace('；',
                                                                                                '\n') if '：' in detail_title else ""
                    elif '预期结果' in detail_title:
                        expected_result = detail_title.split('：', 1)[1].strip().replace('、', '.').replace('；',
                                                                                                          '\n') if '：' in detail_title else ""

                # 添加到Excel数据
                excel_data.append({
                    '模块': module_name,
                    '用例': use_case_name,
                    '前置条件': preconditions,
                    '操作步骤': steps,
                    '预期结果': expected_result
                })

        # 创建DataFrame并保存为Excel
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_file, index=False)

        print(f"转换成功! 已保存到: {excel_file}")
        return True

    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        return False


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='将XMind文件转换为Excel格式')
    # parser.add_argument('input', help='输入的XMind文件路径')
    # parser.add_argument('output', help='输出的Excel文件路径')
    #
    # args = parser.parse_args()
    #
    # if not os.path.exists(args.input):
    #     print(f"错误: 输入文件 '{args.input}' 不存在")
    # else:
    #     xmind_to_excel(args.input, args.output)

    input = r'.\XmindDoc\01_测试思路-脚本替换.xmind'
    output = r'.\ExcelDoc\01_测试思路-脚本替换.xlsx'
    xmind_to_excel(input, output)
