#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门禁协议解析主程序
用于选择不同的协议解析器来解析输入的16进制码流
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser
from bangxun_old_parser import BangxunOldParser
from yingjia_mj200_parser import YingJiaMJ200Parser
from yaa_parser import YaaoParser
from liwei_parser import LiWeiParser
from haineng_parser import HainengParser
from vertiv_parser import VertivParser
from bangxun_new_parser import BangxunNewParser
from tidi_es2200_parser import TidiES2200Parser
from gaoxin_260r_parser import Gaoxin260RParser
from gaoxin_300r_parser import Gaoxin300RParser
from zhongda_chd805_parser import ZhongdaCHD805Parser

class ProtocolParserMain:
    """门禁协议解析主程序"""
    
    def __init__(self):
        self.parsers = {
            "1": {"name": "B接口透传协议", "parser": BInterfaceParser()},
            "2": {"name": "邦讯门禁控制器协议（旧版）", "parser": BangxunOldParser()},
            "3": {"name": "盈佳MJ200门禁协议", "parser": YingJiaMJ200Parser()},
            "4": {"name": "亚奥门禁控制器协议", "parser": YaaoParser()},
            "5": {"name": "力维ACUC3.0门禁控制器协议", "parser": LiWeiParser()},
            "6": {"name": "海能门禁控制器协议", "parser": HainengParser()},
            "7": {"name": "维谛ES2000门禁控制器协议", "parser": VertivParser()},
            "8": {"name": "邦讯门禁控制器协议（新版）", "parser": BangxunNewParser()},
            "9": {"name": "钛迪ES2200门禁控制器协议", "parser": TidiES2200Parser()},
            "10": {"name": "高新兴260R门禁控制器协议", "parser": Gaoxin260RParser()},
            "11": {"name": "高新兴300R门禁控制器协议", "parser": Gaoxin300RParser()},
            "12": {"name": "中达CHD805门禁控制器协议", "parser": ZhongdaCHD805Parser()}
        }
    
    def show_menu(self):
        """显示菜单"""
        print("=== 门禁协议解析器 ===")
        print("注意：所有协议都是UDP类型，外层由B接口包裹")
        print("可以直接选择B接口透传协议解析器来解析包含各种门禁协议的UDP数据包")
        print("\n请选择要使用的协议解析器：")
        for key, value in self.parsers.items():
            print(f"{key}. {value['name']}")
        print("q. 退出程序")
        print("=" * 30)
    
    def get_user_input(self):
        """获取用户输入"""
        while True:
            choice = input("请输入选项：").strip().lower()
            if choice in self.parsers or choice == "q":
                return choice
            else:
                print("无效的选项，请重新输入！")
    
    def get_hex_string(self):
        """获取用户输入的16进制字符串"""
        hex_string = input("请输入16进制码流：").strip()
        return hex_string
    
    def run(self):
        """运行主程序"""
        while True:
            self.show_menu()
            choice = self.get_user_input()
            
            if choice == "q":
                print("退出程序...")
                break
            
            parser_info = self.parsers[choice]
            print(f"\n已选择：{parser_info['name']}")
            
            hex_string = self.get_hex_string()
            if not hex_string:
                print("输入的16进制码流为空，返回主菜单！")
                continue
            
            print("\n正在解析...")
            
            # 检查输入数据是否包含B接口（起始符0xFF）
            try:
                data = bytes.fromhex(hex_string.replace(' ', ''))
                if data[0] == 0xFF and choice != "1":
                    # 包含B接口，自动先使用B接口解析器解析
                    print("检测到B接口封装，自动先解析B接口...")
                    b_parser = BInterfaceParser()
                    b_result = b_parser.parse_packet(hex_string)
                    if isinstance(b_result, dict) and "透传数据解析" in b_result:
                        result = b_result
                    else:
                        # B接口解析失败，再尝试直接用选择的解析器解析
                        result = parser_info["parser"].parse_packet(hex_string)
                else:
                    # 不包含B接口或已选择B接口解析器，直接解析
                    result = parser_info["parser"].parse_packet(hex_string)
            except ValueError:
                # 无效的16进制字符串，直接解析
                result = parser_info["parser"].parse_packet(hex_string)
            
            def format_dict(data, indent=0):
                """递归格式化字典输出"""
                result = []
                indent_str = "  " * indent
                for key, value in data.items():
                    if isinstance(value, dict):
                        result.append(f"{indent_str}{key}:")
                        result.append(format_dict(value, indent + 1))
                    else:
                        result.append(f"{indent_str}{key}: {value}")
                return "\n".join(result)
            
            print("\n解析结果：")
            if isinstance(result, dict):
                print(format_dict(result))
            else:
                print(result)
            
            input("\n按回车键返回主菜单...")
            print("\n" + "=" * 50 + "\n")

# 示例用法
if __name__ == "__main__":
    main = ProtocolParserMain()
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        # 从命令行获取16进制码流
        hex_string = sys.argv[1]
        # 自动使用B接口透传协议解析器
        print(f"=== 自动使用B接口透传协议解析器 ===")
        print(f"输入的16进制码流：{hex_string}")
        print("正在解析...")
        
        # 使用B接口解析器
        b_parser = BInterfaceParser()
        result = b_parser.parse_packet(hex_string)
        
        def format_dict(data, indent=0):
            """递归格式化字典输出"""
            result = []
            indent_str = "  " * indent
            for key, value in data.items():
                if isinstance(value, dict):
                    result.append(f"{indent_str}{key}:")
                    result.append(format_dict(value, indent + 1))
                else:
                    result.append(f"{indent_str}{key}: {value}")
            return "\n".join(result)
        
        print("\n解析结果：")
        if isinstance(result, dict):
            print(format_dict(result))
        else:
            print(result)
    else:
        # 没有命令行参数，运行交互式菜单
        main.run()