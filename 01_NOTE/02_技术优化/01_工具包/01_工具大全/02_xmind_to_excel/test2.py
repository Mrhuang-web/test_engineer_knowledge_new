import pandas as pd
from xmindparser import xmind_to_dict
import argparse
import os


def xmind_to_excel(xmind_file, excel_file):
    try:
        data = xmind_to_dict(xmind_file)

        jsonname = os.path.splitext(os.path.basename(xmind_file))[0]
        os.makedirs('./JsonDoc', exist_ok=True)
        with open(f'./JsonDoc/{jsonname}.json', 'w', encoding='utf-8') as f:
            f.write(str(data).replace("'", '"'))

        central_topic = data[0]['topic']
        excel_data = []

        for module in central_topic['topics']:
            module_name = module['title']
            for use_case in module['topics']:
                use_case_name = use_case['title']

                pre = ''
                steps = ''
                expect = ''

                if 'topics' in use_case:
                    for topic in use_case['topics']:
                        title = topic['title']
                        cleaned = title.replace('、', '.').replace('；', '\n')
                        if '前置条件' in topic['title']:
                            pre = cleaned[5:]
                        elif '操作步骤' in topic['title']:
                            steps = cleaned[5:]
                        elif '预期结果' in topic['title']:
                            expect = cleaned[5:]

                excel_data.append({
                    '模块': module_name,
                    '用例': use_case_name,
                    '前置条件': pre,
                    '操作步骤': steps,
                    '预期结果': expect
                })

        os.makedirs('./ExcelDoc', exist_ok=True)
        pd.DataFrame(excel_data).to_excel(excel_file, index=False)
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

    input = r'.\XmindDoc\01_测试思路_转化模板8[集团-液冷分析报表].xmind'
    output = r'.\ExcelDoc\01_测试思路_转化模板8[集团-液冷分析报表].xlsx'
    xmind_to_excel(input, output)
