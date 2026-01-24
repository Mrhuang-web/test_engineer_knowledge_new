# 只需要禅道的 -- 
# xmind2testcase里面
    zentao.py
    utils.py
    parser.py
    metadata.py
    const.py



# XMind2TestCase


### 二、使用示例

#### 1、Web工具示例

![webtool](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/webtool.png)

#### 2、转换后用例预览

![testcase_preview](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/xmind_to_testcase_preview.png)

#### 3、TestLink导入结果示例

![testlink](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/testlink.png)

#### 4、禅道（ZenTao）导入结果示例

![zentao](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/zentao_import_result.png)


### 三、安装方式
```
pip3 install xmind2testcase
```


### 四、版本升级
```
pip3 install -U xmind2testcase
```


### 五、使用方式

#### 1、命令行调用
```
Usage:
 xmind2testcase [path_to_xmind_file] [-csv] [-xml] [-json]

Example:
 xmind2testcase /path/to/testcase.xmind        => output testcase.csv、testcase.xml、testcase.json
 xmind2testcase /path/to/testcase.xmind -csv   => output testcase.csv
 xmind2testcase /path/to/testcase.xmind -xml   => output testcase.xml
 xmind2testcase /path/to/testcase.xmind -json  => output testcase.json
```

#### 2、使用Web界面

![web_tool_cli](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/webtool_cli.png)

```
Usage:
 xmind2testcase [webtool] [port_num]

Example:
 xmind2testcase webtool        => launch the web testcase convertion tool locally -> 127.0.0.1:5001
 xmind2testcase webtool 8000   => launch the web testcase convertion tool locally -> 127.0.0.1:8000
```

#### 3、API调用
```
import json
import xmind
from xmind2testcase.zentao import xmind_to_zentao_csv_file
from xmind2testcase.testlink import xmind_to_testlink_xml_file
from xmind2testcase.utils import xmind_testcase_to_json_file
from xmind2testcase.utils import xmind_testsuite_to_json_file
from xmind2testcase.utils import get_xmind_testcase_list
from xmind2testcase.utils import get_xmind_testsuite_list


def main():
    xmind_file = 'docs/xmind_testcase_template.xmind'
    print('Start to convert XMind file: %s' % xmind_file)

    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    print('Convert XMind file to zentao csv file successfully: %s' % zentao_csv_file)

    testlink_xml_file = xmind_to_testlink_xml_file(xmind_file)
    print('Convert XMind file to testlink xml file successfully: %s' % testlink_xml_file)

    testsuite_json_file = xmind_testsuite_to_json_file(xmind_file)
    print('Convert XMind file to testsuite json file successfully: %s' % testsuite_json_file)

    testcase_json_file = xmind_testcase_to_json_file(xmind_file)
    print('Convert XMind file to testcase json file successfully: %s' % testcase_json_file)

    testsuites = get_xmind_testsuite_list(xmind_file)
    print('Convert XMind to testsuits dict data:\n%s' % json.dumps(testsuites, indent=2, separators=(',', ': '), ensure_ascii=False))

    testcases = get_xmind_testcase_list(xmind_file)
    print('Convert Xmind to testcases dict data:\n%s' % json.dumps(testcases, indent=4, separators=(',', ': ')))

    workbook = xmind.load(xmind_file)
    print('Convert XMind to Json data:\n%s' % json.dumps(workbook.getData(), indent=2, separators=(',', ': '), ensure_ascii=False))

    print('Finished conversion, Congratulations!')


if __name__ == '__main__':
    main()
```

#### 4、XMind用例文件转为JSON数据

![xmind_testcase_demo](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/xmind_testcase_demo.png)

##### （1）转为TestCase JSON数据

```
from xmind2testcase.utils import get_xmind_testcase_list
xmind_file = 'docs/xmind_testcase_demo.xmind'
testcases = get_xmind_testcase_list(xmind_file)
print(testcases)


Output:

[
    {                                                # 测试用例
        "name": "测试用例1",                           # 用例标题
        "version": 1,                                 # 用例版本
        "summary": "测试用例1",                        # 用例摘要
        "preconditions": "前置条件",                   # 前置条件
        "execution_type": 1,                          # 用例执行类型（1：手动、2：自动）
        "importance": 1,                              # 优先级（1：高、2：中、3：低）
        "estimated_exec_duration": 3,                 # 预计执行时间（分钟）
        "status": 7,                                  # 用例状态（1：草稿、2：待评审、3：评审中、4：重做、5、废弃、6：feature、7：终稿）
        "steps": [                                    # 测试步骤列表
            {
                "step_number": 1,                     # 编号
                "actions": "测试步骤1",                 # 步骤内容
                "expectedresults": "预期结果1",         # 预期结果
                "execution_type": 1                    # 执行类型（1：手动，2：自动）
            }, 
            {
                "step_number": 2, 
                "actions": "测试步骤2", 
                "expectedresults": "预期结果2", 
                "execution_type": 1
            }
        ], 
        "product": "我是产品名",                          # 产品名称
        "suite": "我是模块名(测试集1)"                     # 测试集（模块名）
    }, 
    {
        "name": "测试用例2", 
        "version": 1, 
        "summary": "测试用例2", 
        "preconditions": "前置条件", 
        "execution_type": 1, 
        "importance": 1, 
        "estimated_exec_duration": 3, 
        "status": 7, 
        "steps": [
            {
                "step_number": 1, 
                "actions": "测试步骤1", 
                "expectedresults": "预期结果1", 
                "execution_type": 1
            }, 
            {
                "step_number": 2, 
                "actions": "测试步骤2（预期结果2可以为空）", 
                "expectedresults": "", 
                "execution_type": 1
            }, 
            {
                "step_number": 3, 
                "actions": "测试步骤3", 
                "expectedresults": "预期结果3", 
                "execution_type": 1
            }, 
            {
                "step_number": 4, 
                "actions": "测试步骤4", 
                "expectedresults": "预期结果4", 
                "execution_type": 1
            }
        ], 
        "product": "我是产品名", 
        "suite": "我是模块名(测试集1)"
    }, 
    {
        "name": "测试用例3（测试步骤和预期结果可以都为空）", 
        "version": 1, 
        "summary": "测试用例3（测试步骤和预期结果可以都为空）", 
        "preconditions": "无", 
        "execution_type": 1, 
        "importance": 2, 
        "estimated_exec_duration": 3, 
        "status": 7, 
        "steps": [ ], 
        "product": "我是产品名", 
        "suite": "我是模块名(测试集1)"
    }, 
    {
        "name": "测试步骤2（优先级默认为中）", 
        "version": 1, 
        "summary": "测试步骤2（优先级默认为中）", 
        "preconditions": "无", 
        "execution_type": 1, 
        "importance": 3, 
        "estimated_exec_duration": 3, 
        "status": 7, 
        "steps": [
            {
                "step_number": 1, 
                "actions": "测试步骤1", 
                "expectedresults": "预期结果1", 
                "execution_type": 1
            }, 
            {
                "step_number": 2, 
                "actions": "测试步骤3", 
                "expectedresults": "", 
                "execution_type": 1
            }
        ], 
        "product": "我是产品名", 
        "suite": "我是模块名(测试集2)"
    }, 
    {
        "name": "测试用例3（前置条件默认为空） 无设置优先级，这里加入用例标题", 
        "version": 1, 
        "summary": "测试用例3（前置条件默认为空） 无设置优先级，这里加入用例标题", 
        "preconditions": "无", 
        "execution_type": 1, 
        "importance": 2, 
        "estimated_exec_duration": 3, 
        "status": 7, 
        "steps": [ ], 
        "product": "我是产品名", 
        "suite": "我是模块名(测试集2)"
    }
]
```

测试用例数据增加执行结果字段：result，示例如下：

![测试用例数据](webtool/static/guide/testcase_json_demo.png)

详情查看[使用指南](webtool/static/guide/index.md)，参考示例：[testcase json](docs/xmind_to_testcase_json.json)


##### （2）转为TestSuite JSON数据

```
from xmind2testcase.utils import get_xmind_testsuite_list
xmind_file = 'docs/xmind_testcase_demo.xmind'
testsuites = get_xmind_testsuite_list(xmind_file)
print(testsuites)


Output:

[
  {                                                 # XMind画布（Sheet)列表
    "name": "我是产品名",                             # 产品名称
    "details": null,                                 # 产品摘要
    "testcase_list": [],                             # 用例列表
    "sub_suites": [                                  # 用例集列表
      {
        "name": "我是模块名(测试集1)",                  # 用例集1名称（模块名）
        "details": null,                             # 用例集摘要
        "testcase_list": [                           # 用例列表
          {                                          # 具体用例
            "name": "测试用例1",
            "version": 1,
            "summary": "测试用例1",
            "preconditions": "前置条件",
            "execution_type": 1,
            "importance": 1,
            "estimated_exec_duration": 3,
            "status": 7,
            "steps": [
              {
                "step_number": 1,
                "actions": "测试步骤1",
                "expectedresults": "预期结果1",
                "execution_type": 1
              },
              {
                "step_number": 2,
                "actions": "测试步骤2",
                "expectedresults": "预期结果2",
                "execution_type": 1
              }
            ]
          },
          {
            "name": "测试用例2",
            "version": 1,
            "summary": "测试用例2",
            "preconditions": "前置条件",
            "execution_type": 1,
            "importance": 1,
            "estimated_exec_duration": 3,
            "status": 7,
            "steps": [
              {
                "step_number": 1,
                "actions": "测试步骤1",
                "expectedresults": "预期结果1",
                "execution_type": 1
              },
              {
                "step_number": 2,
                "actions": "测试步骤2（预期结果2可以为空）",
                "expectedresults": "",
                "execution_type": 1
              },
              {
                "step_number": 3,
                "actions": "测试步骤3",
                "expectedresults": "预期结果3",
                "execution_type": 1
              },
              {
                "step_number": 4,
                "actions": "测试步骤4",
                "expectedresults": "预期结果4",
                "execution_type": 1
              }
            ]
          },
          {
            "name": "测试用例3（测试步骤和预期结果可以都为空）",
            "version": 1,
            "summary": "测试用例3（测试步骤和预期结果可以都为空）",
            "preconditions": "无",
            "execution_type": 1,
            "importance": 2,
            "estimated_exec_duration": 3,
            "status": 7,
            "steps": []
          }
        ],
        "sub_suites": []                            # 用例集中可以包含子用例集（目前只要产品类别下有用例集）
      },
      {
        "name": "我是模块名(测试集2)",                  # 用例集2名称（模块名）
        "details": "测试集摘要（详情）",
        "testcase_list": [
          {
            "name": "测试步骤2（优先级默认为中）",
            "version": 1,
            "summary": "测试步骤2（优先级默认为中）",
            "preconditions": "无",
            "execution_type": 1,
            "importance": 3,
            "estimated_exec_duration": 3,
            "status": 7,
            "steps": [
              {
                "step_number": 1,
                "actions": "测试步骤1",
                "expectedresults": "预期结果1",
                "execution_type": 1
              },
              {
                "step_number": 2,
                "actions": "测试步骤3",
                "expectedresults": "",
                "execution_type": 1
              }
            ]
          },
          {
            "name": "测试用例3（前置条件默认为空） 无设置优先级，这里加入用例标题",
            "version": 1,
            "summary": "测试用例3（前置条件默认为空） 无设置优先级，这里加入用例标题",
            "preconditions": "无",
            "execution_type": 1,
            "importance": 2,
            "estimated_exec_duration": 3,
            "status": 7,
            "steps": []
          }
        ],
        "sub_suites": []
      }
    ]
  }
]
```

TestSuite增加执行结果统计字段：statistics，示例如下：

![测试用例数据](webtool/static/guide/testsuite_json_demo.png)

参考示例：[testsuite json](docs/xmind_to_testsuite_json.json)


##### （3）XMind文件转换为JSON数据

以上（1）TestCase数据、（2）TestSuite数据的获取，其实是基于**[XMind](https://github.com/zhuifengshen/xmind)**这个工具，对XMind文件进行解析和数据提取，然后转换而来。
这个工具是在设计XMind2TestCase时，针对XMind单独抽取出来的库，提供了XMind思维导图创建、解析、更新的一系列方法。使用它可以直接将XMind文件转换为JSON数据：

```
import xmind
xmind_file = 'docs/xmind_testcase_demo.xmind'
workbook = xmind.load(xmind_file)
data = workbook.getData()
print(data)


Output:

[
  {                                                    # XMind画布(sheet)列表
    "id": "7hmnj6ahp0lonp4k2hodfok24f",                # 画布ID
    "title": "画布 1",                                  # 画布名称
    "topic": {                                         # 中心主题
      "id": "7c8av5gt8qfbac641lth4g1p67",              # 主题ID
      "link": null,                                    # 主题上的超链接信息
      "title": "我是产品名",                             # 主题名称
      "note": null,                                    # 主题上的备注信息
      "label": null,                                   # 主题上标签信息
      "comment": null,                                 # 主题上的批注（评论）信息
      "markers": [],                                   # 主题上的图标信息
      "topics": [                                      # 子主题列表
        {
          "id": "2rj4ek3nn4sk0lc4pje3gvgv9k",
          "link": null,
          "title": "我是模块名(测试集1)",                  # 子主题1
          "note": null,
          "label": null,
          "comment": null,
          "markers": [],
          "topics": [                                    # 子主题下的子主题列表
            {
              "id": "3hjj43s7rv66uncr1srl3qsboi",
              "link": null,
              "title": "测试用例1",
              "note": "前置条件\n",
              "label": "手动（执行方式默认为手动）",
              "comment": null,
              "markers": [
                "priority-1"
              ],
              "topics": [
                {
                  "id": "3djn37j1fdc6081de319slf035",
                  "link": null,
                  "title": "测试步骤1",
                  "note": null,
                  "label": null,
                  "comment": null,
                  "markers": [],
                  "topics": [
                    {
                      "id": "7v0f1152popou38ndaaamt49l5",
                      "link": null,
                      "title": "预期结果1",
                      "note": null,
                      "label": null,
                      "comment": null,
                      "markers": []
                    }
                  ]
                },
                {
                  "id": "2srtqqjp818clkk1drm233lank",
                  "link": null,
                  "title": "测试步骤2",
                  "note": null,
                  "label": null,
                  "comment": null,
                  "markers": [],
                  "topics": [
                    {
                      "id": "4jlbo280urmid3qkd01j7h8jnq",
                      "link": null,
                      "title": "预期结果2",
                      "note": null,
                      "label": null,
                      "comment": null,
                      "markers": []
                    }
                  ]
                }
              ]
            },
            ...
          ]
        },
        ...
      ]
    }
  }
]
```
具体参考：[xmind_testcase_demo.json](https://github.com/zhuifengshen/xmind2testcase/blob/master/docs/xmind_testcase_demo.json)

