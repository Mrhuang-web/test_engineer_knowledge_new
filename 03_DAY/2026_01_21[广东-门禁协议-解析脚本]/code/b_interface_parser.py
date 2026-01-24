#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B接口透传协议解析脚本
用于解析B接口透传协议的16进制码流，支持上行（FSU→SC）和下行（SC→FSU）两个方向
"""

class BInterfaceParser:
    """B接口透传协议解析器"""
    
    def __init__(self):
        self.header = 0xFF
        self.tailer = 0xFE
        self.escape_char = 0xFD
        self.escape_map = {
            0xFF: b'\xFD\x00',
            0xFE: b'\xFD\x01',
            0xFD: b'\xFD\x02'
        }
        self.unescape_map = {
            b'\x00': 0xFF,
            b'\x01': 0xFE,
            b'\x02': 0xFD
        }
    
    def unescape(self, data):
        """对数据进行解转义处理"""
        result = bytearray()
        i = 0
        while i < len(data):
            if data[i] == self.escape_char and i + 1 < len(data):
                result.append(self.unescape_map[data[i+1:i+2]])
                i += 2
            else:
                result.append(data[i])
                i += 1
        return result
    
    def calculate_checksum(self, data):
        """计算校验和（异或校验）"""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum
    
    def _ascii_hex_to_bytes(self, ascii_hex):
        """将ASCII码表示的十六进制字符串转换为字节流
        例如：b'7E3130' -> b'\x7E\x31\x30'
        """
        try:
            # 将ASCII字符转换为十六进制字符串，然后转换为字节流
            return bytes.fromhex(ascii_hex.decode('ascii'))
        except (ValueError, UnicodeDecodeError) as e:
            return None, f"ASCII转十六进制失败：{e}"
    
    def parse_packet(self, hex_string):
        """解析B接口透传协议数据包"""
        # 将16进制字符串转换为字节流
        try:
            data = bytes.fromhex(hex_string.replace(' ', ''))
        except ValueError as e:
            return f"解析错误：无效的16进制字符串 - {e}"
        
        # 检查数据包长度
        if len(data) < 40:  # 最小数据包长度
            return "解析错误：数据包长度不足"
        
        # 检查包头和包尾
        if data[0] != self.header or data[-1] != self.tailer:
            return "解析错误：包头或包尾不正确"
        
        # 提取RtnFlag字段判断方向
        rtn_flag = data[33]
        if rtn_flag == 0xEE:  # 下行方向（SC→FSU）
            return self._parse_downlink(data)
        elif rtn_flag == 0x00:  # 上行方向（FSU→SC）
            return self._parse_uplink(data)
        elif rtn_flag == 0xED:  # 心跳包
            return self._parse_heartbeat(data)
        else:
            return f"解析错误：未知的RtnFlag值（0x{rtn_flag:02X}）"
    
    def _parse_downlink(self, data):
        """解析下行方向（SC→FSU）数据包"""
        # 下行方向（SC→FSU）格式：
        # 0: P_header (1 byte)
        # 1-20: P_dest_addr (20 bytes)
        # 21-28: P_src_addr (8 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 透传数据长度 (2 bytes)
        # 38-(38+N-1): 透传数据 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 计算透传数据长度，尝试使用little-endian字节序
        transparent_data_len_big = int.from_bytes(data[36:38], byteorder='big')
        transparent_data_len_little = int.from_bytes(data[36:38], byteorder='little')
        
        # 计算实际的透传数据长度（从38字节到倒数第二个字节）
        actual_transparent_data_len = len(data) - 38 - 2  # 总长度 - 固定部分(38) - 校验和(1) - 包尾(1)
        
        # 选择合适的透传数据长度
        if actual_transparent_data_len > 0:
            transparent_data_len = actual_transparent_data_len
        else:
            # 如果计算结果不合理，尝试使用little-endian
            transparent_data_len = transparent_data_len_little
        
        result = {
            "方向": "下行（SC→FSU）",
            "包头": f"0x{data[0]:02X}",
            "目标设备地址": data[1:21].decode('ascii', errors='replace').strip('\x00'),
            "目标设备地址（十六进制）": data[1:21].hex(),
            "源设备地址": data[21:29].decode('ascii', errors='replace').strip('\x00'),
            "源设备地址（十六进制）": data[21:29].hex(),
            "子设备类型": data[29],
            "子设备类型描述": self._get_subdev_type_desc(data[29]),
            "透传模块": f"0x{data[30]:02X}",
            "协议族数据包长度": int.from_bytes(data[31:33], byteorder='big'),
            "设置/应答类型": f"0x{data[33]:02X}",
            "设置/应答类型描述": self._get_rtn_flag_desc(data[33]),
            "命令编号": int.from_bytes(data[34:36], byteorder='big'),
            "命令编号描述": self._get_command_desc(int.from_bytes(data[34:36], byteorder='big')),
            "透传数据长度（大端）": transparent_data_len_big,
            "透传数据长度（小端）": transparent_data_len_little,
            "透传数据长度（实际）": actual_transparent_data_len,
            "透传数据": data[38:-2].hex(),
            "校验和": f"0x{data[-2]:02X}",
            "包尾": f"0x{data[-1]:02X}"
        }
        
        # 验证校验和
        checksum_data = data[1:-2]  # 不包含包头和包尾
        calculated_checksum = self.calculate_checksum(checksum_data)
        result["校验和验证"] = "通过" if calculated_checksum == data[-2] else "失败"
        
        # 解析透传数据
        result["透传数据解析"] = self._parse_transparent_data(data[38:-2])
        
        return result
    
    def _parse_uplink(self, data):
        """解析上行方向（FSU→SC）数据包"""
        # 上行方向（FSU→SC）格式：
        # 0: P_header (1 byte)
        # 1-8: P_dest_addr (8 bytes)
        # 9-28: P_src_addr (20 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 透传数据长度 (2 bytes)
        # 38-(38+N-1): 透传数据 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 计算透传数据长度，尝试使用little-endian字节序
        transparent_data_len_big = int.from_bytes(data[36:38], byteorder='big')
        transparent_data_len_little = int.from_bytes(data[36:38], byteorder='little')
        
        # 计算实际的透传数据长度（从38字节到倒数第二个字节）
        actual_transparent_data_len = len(data) - 38 - 2  # 总长度 - 固定部分(38) - 校验和(1) - 包尾(1)
        
        result = {
            "方向": "上行（FSU→SC）",
            "包头": f"0x{data[0]:02X}",
            "目标设备地址": data[1:9].decode('ascii', errors='replace').strip('\x00'),
            "目标设备地址（十六进制）": data[1:9].hex(),
            "源设备地址": data[9:29].decode('ascii', errors='replace').strip('\x00'),
            "源设备地址（十六进制）": data[9:29].hex(),
            "子设备类型": data[29],
            "子设备类型描述": self._get_subdev_type_desc(data[29]),
            "透传模块": f"0x{data[30]:02X}",
            "协议族数据包长度": int.from_bytes(data[31:33], byteorder='big'),
            "设置/应答类型": f"0x{data[33]:02X}",
            "设置/应答类型描述": self._get_rtn_flag_desc(data[33]),
            "命令编号": int.from_bytes(data[34:36], byteorder='big'),
            "命令编号描述": self._get_command_desc(int.from_bytes(data[34:36], byteorder='big')),
            "透传数据长度（大端）": transparent_data_len_big,
            "透传数据长度（小端）": transparent_data_len_little,
            "透传数据长度（实际）": actual_transparent_data_len,
            "透传数据": data[38:-2].hex(),
            "校验和": f"0x{data[-2]:02X}",
            "包尾": f"0x{data[-1]:02X}"
        }
        
        # 验证校验和
        checksum_data = data[1:-2]  # 不包含包头和包尾
        calculated_checksum = self.calculate_checksum(checksum_data)
        result["校验和验证"] = "通过" if calculated_checksum == data[-2] else "失败"
        
        # 解析透传数据
        result["透传数据解析"] = self._parse_transparent_data(data[38:-2])
        
        return result
    
    def _parse_heartbeat(self, data):
        """解析心跳包"""
        # 心跳包格式：
        # 0: P_header (1 byte)
        # 1-8: P_addr (8 bytes)
        # 9-28: P_src_addr (20 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommandType (2 bytes)
        # 36: P_verify (1 byte)
        # 37: P_tailer (1 byte)
        
        # 检查数据包长度
        if len(data) != 38:
            return f"解析错误：心跳包长度不符，预期38字节，实际{len(data)}字节"
        
        result = {
            "方向": "心跳包（FSU→SC）",
            "包头": f"0x{data[0]:02X}",
            "目标设备地址": data[1:9].decode('ascii', errors='replace').strip('\x00'),
            "目标设备地址（十六进制）": data[1:9].hex(),
            "源设备地址": data[9:29].decode('ascii', errors='replace').strip('\x00'),
            "源设备地址（十六进制）": data[9:29].hex(),
            "子设备类型": data[29],
            "子设备类型描述": self._get_subdev_type_desc(data[29]),
            "透传模块": f"0x{data[30]:02X}",
            "协议族数据包长度": int.from_bytes(data[31:33], byteorder='big'),
            "设置/应答类型": f"0x{data[33]:02X}",
            "设置/应答类型描述": self._get_rtn_flag_desc(data[33]),
            "命令编号": int.from_bytes(data[34:36], byteorder='big'),
            "命令编号描述": self._get_command_desc(int.from_bytes(data[34:36], byteorder='big')),
            "校验和": f"0x{data[36]:02X}",
            "包尾": f"0x{data[37]:02X}"
        }
        
        # 验证校验和
        checksum_data = data[1:36]  # 不包含包头和包尾
        calculated_checksum = self.calculate_checksum(checksum_data)
        result["校验和验证"] = "通过" if calculated_checksum == data[36] else "失败"
        
        return result
    
    def _parse_transparent_data(self, transparent_data):
        """解析透传数据，根据数据特征自动识别并调用相应的协议解析器"""
        result = {
            "透传数据长度": len(transparent_data),
            "透传数据（十六进制）": transparent_data.hex(),
            "透传数据（ASCII）": transparent_data.decode('ascii', errors='replace')
        }
        
        if len(transparent_data) == 0:
            result["协议类型"] = "空数据"
            return result
        
        # 首先尝试直接解析原始透传数据，检查是否为各种协议
        # 原始透传数据可能是ASCII字符串，也可能包含非ASCII字符
        try:
            ascii_str = transparent_data.decode('ascii')
            result["原始ASCII字符串"] = ascii_str
            
            # 提取十六进制部分（去掉~和\r\n）
            hex_str = ascii_str.strip('~\r\n')
            result["提取的十六进制字符串"] = hex_str
            
            # 检查提取的十六进制字符串是否符合邦讯协议特征（命令号范围0x1000-0x10FF）
            if len(hex_str) >= 4:  # 至少需要4个字符（2字节命令号）
                # 转换前4个字符为命令号
                command_str = hex_str[:4]
                try:
                    command = int(command_str, 16)
                    if 0x1000 <= command <= 0x10FF:
                        # 符合邦讯协议命令号范围，直接使用邦讯解析器
                        result["协议类型"] = "邦讯门禁控制器协议（命令号范围0x1000-0x10FF）"
                        from bangxun_new_parser import BangxunNewParser
                        parser = BangxunNewParser()
                        # 使用完整的十六进制字符串进行解析
                        parse_result = parser.parse_packet(hex_str)
                        if isinstance(parse_result, dict):
                            result["协议详细解析"] = parse_result
                        else:
                            result["协议解析错误"] = parse_result
                        return result
                except ValueError:
                    pass  # 不是有效的十六进制命令号，继续检查其他协议
            
            # 检查提取的十六进制字符串是否为其他协议
            if hex_str:
                try:
                    # 将十六进制字符串转换为实际的协议数据字节流
                    actual_protocol_data = bytes.fromhex(hex_str)
                    result["转换后的透传数据（十六进制）"] = actual_protocol_data.hex()
                    
                    # 现在根据转换后的实际协议数据进行协议识别
                    # 1. 检查是否为盈佳MJ200门禁协议（6字节起始符）
                    if len(actual_protocol_data) >= 6 and actual_protocol_data[:6] == b'\xFA\x55\xFA\x55\xFA\x55':
                        result["协议类型"] = "盈佳MJ200门禁协议（起始符0xFA55FA55FA55）"
                        from yingjia_mj200_parser import YingJiaMJ200Parser
                        parser = YingJiaMJ200Parser()
                        parse_result = parser.parse_packet(actual_protocol_data.hex())
                        if isinstance(parse_result, dict):
                            result["协议详细解析"] = parse_result
                        else:
                            result["协议解析错误"] = parse_result
                        return result
                    
                    # 2. 检查是否为亚奥门禁协议（起始符0x55）
                    elif actual_protocol_data[0] == 0x55:
                        result["协议类型"] = "亚奥门禁控制器协议（起始符0x55）"
                        from yaa_parser import YaaoParser
                        parser = YaaoParser()
                        parse_result = parser.parse_packet(actual_protocol_data.hex())
                        if isinstance(parse_result, dict):
                            result["协议详细解析"] = parse_result
                        else:
                            result["协议解析错误"] = parse_result
                        return result
                    
                    # 3. 检查是否为海能门禁协议（起始符0x68）
                    elif actual_protocol_data[0] == 0x68:
                        result["协议类型"] = "海能门禁控制器协议（起始符0x68）"
                        from haineng_parser import HainengParser
                        parser = HainengParser()
                        parse_result = parser.parse_packet(actual_protocol_data.hex())
                        if isinstance(parse_result, dict):
                            result["协议详细解析"] = parse_result
                        else:
                            result["协议解析错误"] = parse_result
                        return result
                    
                    # 4. 检查是否为BASS/力维/高新兴/维谛/钛迪/中达等协议（起始符0x7E）
                    elif actual_protocol_data[0] == 0x7E:
                        result["协议类型"] = "以0x7E开头的门禁协议（中达/力维/高新兴/维谛/钛迪）"
                        
                        # 检查版本号字段（第2字节）
                        if len(actual_protocol_data) >= 2:
                            ver = actual_protocol_data[1]
                            
                            if ver == 0x20:  # 高新兴260R协议版本号V2.1
                                result["协议类型"] = "高新兴260R门禁控制器协议（版本号0x20）"
                                from gaoxin_260r_parser import Gaoxin260RParser
                                parser = Gaoxin260RParser()
                                parse_result = parser.parse_packet(actual_protocol_data.hex())
                                if isinstance(parse_result, dict):
                                    result["协议详细解析"] = parse_result
                                else:
                                    result["协议解析错误"] = parse_result
                            elif ver == 0x10:  # 力维、维谛、钛迪、中达等协议版本号V1.0
                                # 根据CID1字段进一步区分
                                if len(actual_protocol_data) >= 4:
                                    cid1 = actual_protocol_data[3]
                                    device_type = (cid1 >> 4) & 0x0F
                                    
                                    if device_type == 0x08:  # 门禁控制类
                                        result["协议类型"] = "中达CHD805等门禁控制类协议（CID1=0x80）"
                                        from zhongda_chd805_parser import ZhongdaCHD805Parser
                                        parser = ZhongdaCHD805Parser()
                                        parse_result = parser.parse_packet(actual_protocol_data.hex())
                                        if isinstance(parse_result, dict):
                                            result["协议详细解析"] = parse_result
                                        else:
                                            result["协议解析错误"] = parse_result
                            else:  # 其他版本号
                                # 尝试使用中达CHD805解析器作为通用解析器
                                result["协议类型"] = f"门禁控制类协议（版本号0x{ver:02X}）"
                                from zhongda_chd805_parser import ZhongdaCHD805Parser
                                parser = ZhongdaCHD805Parser()
                                parse_result = parser.parse_packet(actual_protocol_data.hex())
                                if isinstance(parse_result, dict):
                                    result["协议详细解析"] = parse_result
                                else:
                                    result["协议解析错误"] = parse_result
                        return result
                except ValueError as e:
                    result["转换错误"] = f"十六进制字符串转换失败：{e}"
        except UnicodeDecodeError as e1:
            result["转换错误"] = f"无法将透传数据解码为ASCII字符串：{e1}"
            
            # 备选方案：直接处理透传数据的十六进制表示，两位两位地解析
            # 透传数据本身是十六进制形式，例如：7e79f781100000000000000000000000000000000000000000000001020d
            # 我们需要两位两位地提取，形成实际的协议数据
            try:
                # 获取透传数据的十六进制表示
                transparent_hex = transparent_data.hex()
                result["透传数据十六进制表示"] = transparent_hex
                
                # 两位两位地解析，跳过起始的7e（如果存在）
                if transparent_hex.startswith('7e'):
                    actual_hex_str = transparent_hex[2:]  # 跳过起始的7e
                else:
                    actual_hex_str = transparent_hex
                
                # 确保字符串长度为偶数
                if len(actual_hex_str) % 2 != 0:
                    actual_hex_str = actual_hex_str[:-1]  # 移除最后一个字符
                
                # 转换为实际的协议数据字节流
                actual_protocol_data = bytes.fromhex(actual_hex_str)
                result["转换后的透传数据（十六进制）"] = actual_protocol_data.hex()
                
                # 现在根据转换后的实际协议数据进行协议识别
                # 1. 检查是否为盈佳MJ200门禁协议（6字节起始符）
                if len(actual_protocol_data) >= 6 and actual_protocol_data[:6] == b'\xFA\x55\xFA\x55\xFA\x55':
                    result["协议类型"] = "盈佳MJ200门禁协议（起始符0xFA55FA55FA55）"
                    from yingjia_mj200_parser import YingJiaMJ200Parser
                    parser = YingJiaMJ200Parser()
                    parse_result = parser.parse_packet(actual_protocol_data.hex())
                    if isinstance(parse_result, dict):
                        result["协议详细解析"] = parse_result
                    else:
                        result["协议解析错误"] = parse_result
                    return result
                
                # 2. 检查是否为亚奥门禁协议（起始符0x55）
                elif actual_protocol_data[0] == 0x55:
                    result["协议类型"] = "亚奥门禁控制器协议（起始符0x55）"
                    from yaa_parser import YaaoParser
                    parser = YaaoParser()
                    parse_result = parser.parse_packet(actual_protocol_data.hex())
                    if isinstance(parse_result, dict):
                        result["协议详细解析"] = parse_result
                    else:
                        result["协议解析错误"] = parse_result
                    return result
                
                # 3. 检查是否为海能门禁协议（起始符0x68）
                elif actual_protocol_data[0] == 0x68:
                    result["协议类型"] = "海能门禁控制器协议（起始符0x68）"
                    from haineng_parser import HainengParser
                    parser = HainengParser()
                    parse_result = parser.parse_packet(actual_protocol_data.hex())
                    if isinstance(parse_result, dict):
                        result["协议详细解析"] = parse_result
                    else:
                        result["协议解析错误"] = parse_result
                    return result
                
                # 4. 检查是否为BASS/力维/高新兴/维谛/钛迪/中达等协议（起始符0x7E）
                elif actual_protocol_data[0] == 0x7E:
                    result["协议类型"] = "以0x7E开头的门禁协议（中达/力维/高新兴/维谛/钛迪）"
                    
                    # 检查版本号字段（第2字节）
                    if len(actual_protocol_data) >= 2:
                        ver = actual_protocol_data[1]
                        
                        if ver == 0x20:  # 高新兴260R协议版本号V2.1
                            result["协议类型"] = "高新兴260R门禁控制器协议（版本号0x20）"
                            from gaoxin_260r_parser import Gaoxin260RParser
                            parser = Gaoxin260RParser()
                            parse_result = parser.parse_packet(actual_protocol_data.hex())
                            if isinstance(parse_result, dict):
                                result["协议详细解析"] = parse_result
                            else:
                                result["协议解析错误"] = parse_result
                        elif ver == 0x10:  # 力维、维谛、钛迪、中达等协议版本号V1.0
                            # 根据CID1字段进一步区分
                            if len(actual_protocol_data) >= 4:
                                cid1 = actual_protocol_data[3]
                                device_type = (cid1 >> 4) & 0x0F
                                
                                if device_type == 0x08:  # 门禁控制类
                                    result["协议类型"] = "中达CHD805等门禁控制类协议（CID1=0x80）"
                                    from zhongda_chd805_parser import ZhongdaCHD805Parser
                                    parser = ZhongdaCHD805Parser()
                                    parse_result = parser.parse_packet(actual_protocol_data.hex())
                                    if isinstance(parse_result, dict):
                                        result["协议详细解析"] = parse_result
                                    else:
                                        result["协议解析错误"] = parse_result
                        else:  # 其他版本号
                            # 尝试使用中达CHD805解析器作为通用解析器
                            result["协议类型"] = f"门禁控制类协议（版本号0x{ver:02X}）"
                            from zhongda_chd805_parser import ZhongdaCHD805Parser
                            parser = ZhongdaCHD805Parser()
                            parse_result = parser.parse_packet(actual_protocol_data.hex())
                            if isinstance(parse_result, dict):
                                result["协议详细解析"] = parse_result
                            else:
                                result["协议解析错误"] = parse_result
                    return result
                
                # 5. 检查是否为邦讯协议（命令号范围0x1000-0x10FF）
                elif len(actual_protocol_data) >= 2:
                    command = int.from_bytes(actual_protocol_data[0:2], byteorder='big')
                    if 0x1000 <= command <= 0x10FF:
                        result["协议类型"] = "邦讯门禁控制器协议（命令号范围0x1000-0x10FF）"
                        from bangxun_new_parser import BangxunNewParser
                        parser = BangxunNewParser()
                        parse_result = parser.parse_packet(actual_protocol_data.hex())
                        if isinstance(parse_result, dict):
                            result["协议详细解析"] = parse_result
                        else:
                            result["协议解析错误"] = parse_result
                        return result
            except ValueError as e2:
                result["备选解析错误"] = f"两位两位解析失败：{e2}"
            except Exception as e3:
                result["备选解析错误"] = f"备选解析过程中发生错误：{str(e3)}"
        
        # 如果以上解析都失败，尝试直接解析原始透传数据
        result["协议类型"] = "未知协议类型"
        result["协议解析"] = "无法识别的协议格式"
        
        return result
    
    def _get_subdev_type_desc(self, subdev_type):
        """获取子设备类型描述"""
        type_map = {
            1: "串口设备",
            2: "USB设备",
            3: "IP网络设备"
        }
        return type_map.get(subdev_type, f"未知类型（0x{subdev_type:02X}")
    
    def _get_rtn_flag_desc(self, rtn_flag):
        """获取设置/应答类型描述"""
        flag_map = {
            0xEE: "设置类型（SC→FSU）",
            0x00: "应答类型（FSU→SC）",
            0xED: "心跳包类型（FSU→SC）"
        }
        return flag_map.get(rtn_flag, f"未知类型（0x{rtn_flag:02X}")
    
    def _get_command_desc(self, command):
        """获取命令编号描述"""
        command_map = {
            0x0001: "透传串口数据",
            0x0002: "FSU透传通道心跳"
        }
        return command_map.get(command, f"未知命令（0x{command:04X}")

# 示例用法
if __name__ == "__main__":
    parser = BInterfaceParser()
    
    # 用户提供的示例码流
    user_example = "FF3230323530313132000000000000000000000000300000000000000001001100EE01000C00101001884A0002F2E1F269109DFE"
    
    # 示例下行数据包
    downlink_example = "FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 08 00 00 01 00 02 01 02 EE 00 01 00 02 03 04 07 FE"
    
    # 示例上行数据包
    uplink_example = "FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 08 00 00 01 00 02 01 02 00 00 01 00 02 05 06 0B FE"
    
    print("=== B接口透传协议解析示例 ===")
    
    print("\n用户提供的示例码流：")
    print(user_example)
    result = parser.parse_packet(user_example)
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print(result)
    
    print("\n\n下行数据包示例：")
    result = parser.parse_packet(downlink_example)
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)
    
    print("\n上行数据包示例：")
    result = parser.parse_packet(uplink_example)
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)