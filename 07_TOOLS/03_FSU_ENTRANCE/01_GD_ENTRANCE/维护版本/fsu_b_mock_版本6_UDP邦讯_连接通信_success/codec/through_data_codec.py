#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
透传数据编解码器，用于处理不同厂商设备的透传数据协议
"""

import logging
import random
from typing import Dict, Any, List, Tuple, Optional

from utils.time_utils import TimeFunctionUtils

class ThroughDataCodec:
    """透传数据编解码器"""
    
    def __init__(self, protocol_config: Dict[str, Any]):
        """初始化透传数据编解码器
        
        Args:
            protocol_config: 协议配置
        """
        self.logger = logging.getLogger("codec.through_data")
        self.protocol_config = protocol_config
        self.protocol = protocol_config.get("protocol", {})
        self.vendor = protocol_config.get("vendor", "未知")
        self.vendor_type = protocol_config.get("vendor_type", "")
        
        # 初始化时间函数工具类
        self.time_utils = TimeFunctionUtils()
        
        # 解析协议配置
        self.pdu_left = self.protocol.get("pdu_left", [])
        self.pdu_tailer = self.protocol.get("pdu_tailer", [])
        self.data_frame = self.protocol.get("data_frame", [])
        self.dynamic_length = self.protocol.get("dynamic_length", False)
        self.total_length = self.protocol.get("total_length", 0)
        self.data_frame_type_flag = self.protocol.get("data_frame_type_flag", "data_frame_type")
        
        # 打印初始化信息
        self.logger.debug("透传数据编解码器初始化完成")
        self.logger.debug(f"协议配置: {self.protocol_config}")
        self.logger.debug(f"厂商: {self.vendor}")
        self.logger.debug(f"厂商类型: {self.vendor_type}")
    
    def decode(self, data: bytes) -> Tuple[bool, Dict[str, Any]]:
        """解码透传数据
        
        Args:
            data: 原始数据
            
        Returns:
            (成功标志, 解析结果)
        """
        result = {
            "raw_data": data.hex().upper(),
            "parsed": {
                "through_pdu": {},
                "through_sdu": {}
            }
        }
        
        try:
            if not data:
                self.logger.error("数据为空")
                return False, result
            
            # 检查是否为ASCII编码的十六进制字符串（仅力维类协议需要）
            is_ascii_hex = False
            if self.vendor_type == "liwei" and len(data) > 2 and data[0] == 0x7E and data[-1] == 0x0D:
                # 检查中间是否全部是ASCII字符
                try:
                    # 尝试解码为ASCII字符串
                    ascii_str = data[1:-1].decode('ascii')
                    # 尝试将中间部分转换为十六进制数据，验证是否是有效的十六进制字符串
                    bytes.fromhex(ascii_str)
                    is_ascii_hex = True
                except:
                    pass
            
            # 如果是力维类协议且是ASCII编码的十六进制字符串，转换为二进制数据
            if self.vendor_type == "liwei" and is_ascii_hex:
                self.logger.debug(f"检测到ASCII编码的十六进制字符串，转换为二进制数据")
                # 提取中间的ASCII字符串部分
                ascii_str = data[1:-1].decode('ascii')
                # 转换为二进制数据
                binary_data = bytes.fromhex(ascii_str)
                # 重新构建完整的二进制数据包
                data = bytes([0x7E]) + binary_data + bytes([0x0D])
                self.logger.debug(f"转换后的数据: {data.hex()}")
            
            # 验证数据长度
            if not self.dynamic_length and len(data) != self.total_length:
                self.logger.error(f"数据长度错误: 期望 {self.total_length}, 实际 {len(data)}")
                return False, result
            
            # 解析 PDU_LEFT， 写入到through_pdu
            pdu_left_result, offset = self._parse_fields(data, self.pdu_left, 0)
            result["parsed"]["through_pdu"].update(pdu_left_result)
            
            # 解析 DATA_FRAME
            data_frame_type = ""
            data_frame_config = {}
            data_frame_result = {}
            
            # 步骤1：尝试解析所有可能的数据帧配置，获取完整的数据
            temp_data_frame_result = {}
            temp_offset = offset
            
            # 尝试解析所有data_frame配置，获取完整的数据
            for df_config in self.data_frame:
                req_fields = df_config.get("req_data_list", [])
                
                # 计算该配置需要的数据长度
                required_length = 0
                for field in req_fields:
                    required_length += field.get("length", 0)
                
                # 检查剩余数据是否足够
                if offset + required_length > len(data):
                    continue
                
                # 尝试解析
                temp_result, temp_off = self._parse_fields(data, req_fields, offset)
                if temp_result:
                    # 验证解析结果是否符合配置
                    valid = True
                    for field in req_fields:
                        field_name = field.get("name", "")
                        field_value = field.get("value", "")
                        if field_name in temp_result and field_value:
                            if temp_result[field_name] != bytes.fromhex(field_value).hex().upper():
                                valid = False
                                break
                    
                    if valid:
                        temp_data_frame_result = temp_result
                        temp_offset = temp_off
                        break
            
            # 如果没有匹配到，使用第一个配置
            if not temp_data_frame_result and self.data_frame:
                df_config = self.data_frame[0]
                req_fields = df_config.get("req_data_list", [])
                temp_data_frame_result, temp_offset = self._parse_fields(data, req_fields, offset)
            
            # 写 SDU 解析数据
            result["parsed"]["through_sdu"].update(temp_data_frame_result)
            
            # 步骤2：根据 data_frame_type_flag 模板生成实际的数据帧类型
            data_frame_type = self._generate_data_frame_type(pdu_left_result, temp_data_frame_result)
            self.logger.debug(f"生成的数据帧类型: {data_frame_type}")
            
            # 力维协议特殊处理：如果生成的数据帧类型为空，尝试直接从二进制数据中提取字段
            if self.vendor_type == "liwei" and not data_frame_type:
                self.logger.debug(f"力维协议：生成的数据帧类型为空，尝试直接从二进制数据中提取字段")
                # 从pdu_left_result中获取cid2
                cid2 = pdu_left_result.get("cid2", "")
                # 直接从二进制数据中提取group和type字段
                if len(data) >= offset + 2:
                    group = data[offset:offset+1].hex().upper()
                    type_code = data[offset+1:offset+2].hex().upper()
                    # 构建data_frame_type
                    data_frame_type = f"{cid2}_{group}_{type_code}"
                    self.logger.debug(f"直接从二进制数据中提取的data_frame_type: {data_frame_type}")
            
            # 步骤3：根据生成的数据帧类型查找配置
            data_frame_config = self._get_data_frame_config(data_frame_type)
            if data_frame_config:
                # 找到配置，更新偏移量
                offset = temp_offset
            else:
                # 没找到配置，尝试使用第一个配置
                self.logger.warning(f"未找到数据帧类型 {data_frame_type} 的配置，尝试使用第一个配置")
                if self.data_frame:
                    data_frame_config = self.data_frame[0]
                else:
                    self.logger.error("没有数据帧配置可用")
                    return False, result
            
            self.logger.debug(f"最终获取的数据帧类型: {data_frame_type}, 数据帧配置: {data_frame_config}")
            
            # 根据协议配置解析PDU_TAILER 写入到 PDU
            # 如果pdu_tailer为空或只有checksum和end字段，直接提取
            if not self.pdu_tailer or (len(self.pdu_tailer) == 2 and 
                                     any(field["name"] == "checksum" for field in self.pdu_tailer) and 
                                     any(field["name"] == "end" for field in self.pdu_tailer)):
                # 直接从剩余数据中提取checksum和end
                # 从配置中获取checksum和end字段的长度
                checksum_length = 1  # 默认值
                end_length = 1  # 默认值
                
                for field in self.pdu_tailer:
                    if field["name"] == "checksum":
                        checksum_length = field.get("length", 1)
                    elif field["name"] == "end":
                        end_length = field.get("length", 1)
                
                if len(data) >= offset + checksum_length + end_length:
                    checksum = data[offset:offset+checksum_length].hex().upper()
                    end = data[offset+checksum_length:offset+checksum_length+end_length].hex().upper()
                    pdu_tailer_result = {
                        "checksum": checksum,
                        "end": end
                    }
                    result["parsed"]["through_pdu"].update(pdu_tailer_result)
            else:
                # 正常解析PDU_TAILER
                pdu_tailer_result, _ = self._parse_fields(data, self.pdu_tailer, offset)
                result["parsed"]["through_pdu"].update(pdu_tailer_result)
            
            return True, result
            
        except Exception as e:
            self.logger.error(f"解码失败: {str(e)}")
            return False, result
    
    def encode(self, parsed_data: Dict[str, Any], response_data: Dict[str, Any]) -> bytes:
        """编码透传数据
        
        Args:
            parsed_data: 解析后的数据
            response_data: 响应数据
            
        Returns:
            编码后的数据
        """
        try:
            self.logger.debug(f"开始编码透传数据")
            self.logger.debug(f"解析后的数据: {parsed_data}")
            self.logger.debug(f"响应数据: {response_data}")
            
            # 获取数据帧类型和数据帧配置（这步必须在编码pdu_left之前）
            data_frame_type = self._get_data_frame_type_from_parsed(parsed_data)
            self.logger.debug(f"生成的数据帧类型: {data_frame_type}")
            
            data_frame_config = self._get_data_frame_config(data_frame_type)
            self.logger.debug(f"数据帧配置: {data_frame_config}")
            
            if not data_frame_config:
                self.logger.error(f"未找到数据帧类型 {data_frame_type} 的配置")
                return b""
            
            # 编码 DATA_FRAME
            resp_fields = data_frame_config.get("resp_data_list", [])
            data_frame_data = b""
            
            # 力维协议特殊处理：优先使用用户传入的response_data
            if self.vendor_type == "liwei" and response_data:
                # 如果用户传入了response_data，根据用户数据构建响应
                self.logger.debug(f"力维协议：优先使用用户传入的response_data构建响应")

                # 检查是否是远程监控请求
                group = response_data.get("group", "")
                type_code = response_data.get("type", "")
                dataf = response_data.get("dataf", "00")
                
                # 处理远程监控(0XE7)请求
                if group == "F2" and type_code == "E7" and dataf == "00":
                    self.logger.debug("力维协议：处理远程监控(0XE7)请求")
                    
                    # 从配置或response_data中获取工作状态和线路状态
                    work_status = 0x00
                    line_status = 0x00
                    
                    # 尝试从response_data中获取
                    if "work_status" in response_data:
                        work_status = int(response_data["work_status"], 16) if isinstance(response_data["work_status"], str) else response_data["work_status"]
                    if "line_status" in response_data:
                        line_status = int(response_data["line_status"], 16) if isinstance(response_data["line_status"], str) else response_data["line_status"]
                    
                    # 构建INFO数据：工作状态 + 线路状态
                    info_data = bytes([work_status, line_status])
                    
                    # 保存INFO数据，供后续校验和计算使用
                    self._liwei_info_data = info_data
                    
                    # 构建data_frame_data：group + type + dataf + 工作状态 + 线路状态
                    data_frame_data = bytes.fromhex(group + type_code + dataf) + info_data
                    
                    # 确保响应格式与f0,e0不同，根据协议返回正确的响应
                    self.logger.debug(f"远程监控(0XE7)响应: 工作状态=0x{work_status:02X}, 线路状态=0x{line_status:02X}")
                    self.logger.debug(f"构建的data_frame_data: {data_frame_data.hex().upper()}")
                    self.logger.debug(f"保存的INFO数据: {self._liwei_info_data.hex().upper()}")
                
                # 处理远程监控(0XED)请求
                elif group == "F1" and type_code == "ED" and dataf == "00":
                    self.logger.debug("力维协议：处理远程监控(0XED)请求")
                    
                    # 构建控制状态字节 (第1字节)
                    # D7=0: 门常开无效
                    # D6=0: 门常闭无效
                    # D5=0: 第2继电器未动作
                    # D4=0: 紧急输入无效
                    # D3=0: 门磁不监控
                    # D2=0: 红外感应器不监控
                    # D1=0: 门控继电器未动作
                    # D0=0: 正常，无报警输出
                    control_status = 0x00
                    
                    # 构建感应头状态字节 (第2字节)
                    # D7=0: 第二感应头对应控制(门)的状态
                    # D6=0: IR/ID或联动
                    # D5=0: HANDLE或联动
                    # D4=0:
                    # D3=0: 第一感应头对应控制(门)的状态
                    # D2=0: IR/ID
                    # D1=0: HANDLE
                    # D0=0:
                    sensor_status = 0x00
                    
                    # 获取SAVEP、LOADP、MF（从记录区管理器）
                    savep = response_data.get("savep", 0)
                    loadp = response_data.get("loadp", 0)
                    mf = response_data.get("mf", 0)
                    
                    # 直接构建响应数据
                    # 格式：group + type + dataf + 控制状态 + 感应头状态 + SAVEP(2字节) + LOADP(2字节) + MF(1字节)
                    data_frame_data = bytes.fromhex(group + type_code + dataf) + bytes([
                        control_status,
                        sensor_status,
                        (savep >> 8) & 0xFF,  # SAVEP高字节
                        savep & 0xFF,          # SAVEP低字节
                        (loadp >> 8) & 0xFF,   # LOADP高字节
                        loadp & 0xFF,          # LOADP低字节
                        mf                     # MF
                    ])
                
                # 处理其他力维协议请求
                else:
                    # 构建力维协议INFO部分数据
                    info_data = b""

                    # 按照力维协议格式顺序添加字段：事件来源(5) + 日期时间(7) + 状态(1) + 备注(1)
                    field_order = ["event_source", "year", "month", "day", "hour", "minute", "second", "status", "remark"]

                    for field_name in field_order:
                        if field_name in response_data:
                            value = response_data[field_name]
                            # 根据字段名确定长度
                            if field_name == "year":
                                # 年份：2字节BCD格式
                                year_str = str(value)
                                if len(year_str) == 4:
                                    # 转换为BCD格式
                                    bcd_year = ((int(year_str[0]) << 12) | (int(year_str[1]) << 8) | (int(year_str[2]) << 4) | int(year_str[3]))
                                    info_data += bcd_year.to_bytes(2, byteorder='big')
                            elif field_name == "month" or field_name == "day" or field_name == "week" or field_name == "hour" or field_name == "minute" or field_name == "second":
                                # 月、日、周、时、分、秒：1字节BCD格式
                                num = int(value)
                                bcd_value = ((num // 10) << 4) | (num % 10)
                                info_data += bytes([bcd_value])
                            elif field_name == "event_source":
                                # 事件源：5字节
                                if len(value) >= 10:
                                    info_data += bytes.fromhex(value[:10])
                                else:
                                    info_data += bytes.fromhex(value.ljust(10, '0'))
                            elif field_name == "status" or field_name == "remark":
                                # 状态、备注：1字节
                                if isinstance(value, str) and len(value) >= 2:
                                    info_data += bytes.fromhex(value[:2])
                                else:
                                    info_data += bytes([0x00])

                    # 保存INFO数据，供后续校验和计算使用
                    self._liwei_info_data = info_data

                    # 力维协议事件数据：直接使用INFO数据，不处理resp_fields
                    # 避免重复添加数据，确保数据格式正确
                    data_frame_data = info_data
            else:
                # 否则按照配置文件构建响应
                for field in resp_fields:
                    field_data = self._encode_field(field, parsed_data, response_data)
                    data_frame_data += field_data
            
            self.logger.debug(f"DATA_FRAME编码结果: {data_frame_data.hex().upper()}, 长度={len(data_frame_data)}, 字段数={len(resp_fields)}")
            
            # 添加填充数据
            data_frame_length = data_frame_config.get("data_frame_length", 26)
            if data_frame_length > 0:
                padding_length = data_frame_length - len(data_frame_data)
                if padding_length > 0:
                    padding_byte = bytes.fromhex(data_frame_config.get("padding", "00"))
                    padding_data = padding_byte * padding_length
                    data_frame_data += padding_data
                    self.logger.debug(f"添加填充数据: {padding_length} 字节, 填充字节: {padding_byte.hex()}")
            
            # 编码 PDU_LEFT
            pdu_left_data = b""
            for field in self.pdu_left:
                field_data = self._encode_field(field, parsed_data, response_data)
                pdu_left_data += field_data
            self.logger.debug(f"PDU_LEFT编码结果: {pdu_left_data.hex().upper()}, 长度={len(pdu_left_data)}")
            
            # 编码 PDU_TAILER，包含checksum字段（会被后续计算覆盖）
            pdu_tailer_data = b""
            for field in self.pdu_tailer:
                field_data = self._encode_field(field, parsed_data, response_data)
                pdu_tailer_data += field_data
            self.logger.debug(f"PDU_TAILER编码结果: {pdu_tailer_data.hex().upper()}, 长度={len(pdu_tailer_data)}")
            
            # 构建完整数据
            full_data = pdu_left_data + data_frame_data + pdu_tailer_data
            self.logger.debug(f"构建完整数据: {full_data.hex().upper()}, 总长度={len(full_data)}")
            
            # 计算校验和
            full_data = self._calculate_checksum(full_data)
            self.logger.debug(f"计算校验和后的数据: {full_data.hex().upper()}, 总长度={len(full_data)}")
            
            # 如果是力维类协议，将二进制数据转换为ASCII编码的十六进制字符串
            if self.vendor_type == "liwei":
                self.logger.debug(f"{self.vendor}协议编码: 将二进制数据转换为ASCII编码的十六进制字符串")
                self.logger.debug(f"转换前的完整数据: {full_data.hex().upper()}, 长度: {len(full_data)}")
                self.logger.debug(f"起始符: 0x{full_data[0]:X}, 结束符: 0x{full_data[-1]:X}")
                # 移除起始符和结束符，只转换中间的数据
                if len(full_data) >= 2:
                    self.logger.debug(f"数据长度满足条件: {len(full_data)} >= 2")
                    self.logger.debug(f"起始符检查: {full_data[0] == 0x7E}, 0x{full_data[0]:X} == 0x7E")
                    self.logger.debug(f"结束符检查: {full_data[-1] == 0x0D}, 0x{full_data[-1]:X} == 0x0D")
                    
                    if full_data[0] == 0x7E and full_data[-1] == 0x0D:
                        # 提取中间的数据部分
                        middle_data = full_data[1:-1]
                        self.logger.debug(f"中间数据: {middle_data.hex().upper()}, 长度: {len(middle_data)}")
                        # 将中间数据转换为ASCII编码的十六进制字符串（使用大写）
                        ascii_hex = middle_data.hex().upper().encode('ascii')
                        self.logger.debug(f"ASCII编码后的十六进制字符串: {ascii_hex.decode('ascii')}, 长度: {len(ascii_hex)}")
                        # 重新构建完整的数据包：起始符 + ASCII编码的十六进制字符串 + 结束符
                        full_data = bytes([0x7E]) + ascii_hex + bytes([0x0D])
                        self.logger.debug(f"{self.vendor}协议编码结果: {full_data.hex().upper()}, 最终长度: {len(full_data)}")
                    else:
                        self.logger.debug(f"数据不满足ASCII转换条件: 起始符={full_data[0]:X}, 结束符={full_data[-1]:X}")
                        # 强制转换，不依赖结束符检查
                        self.logger.debug(f"力维协议：强制进行ASCII转换")
                        # 提取中间的数据部分（不包括起始符）
                        if len(full_data) >= 1 and full_data[0] == 0x7E:
                            middle_data = full_data[1:]
                        else:
                            middle_data = full_data
                        # 将中间数据转换为ASCII编码的十六进制字符串（使用大写）
                        ascii_hex = middle_data.hex().upper().encode('ascii')
                        self.logger.debug(f"强制ASCII编码后的十六进制字符串: {ascii_hex.decode('ascii')}, 长度: {len(ascii_hex)}")
                        # 重新构建完整的数据包：起始符 + ASCII编码的十六进制字符串 + 结束符
                        full_data = bytes([0x7E]) + ascii_hex + bytes([0x0D])
                        self.logger.debug(f"{self.vendor}协议强制编码结果: {full_data.hex().upper()}, 最终长度: {len(full_data)}")
                else:
                    self.logger.debug(f"数据长度不满足条件: {len(full_data)} < 2")
            
            self.logger.debug(f"最终编码结果: {full_data.hex().upper()}, 长度: {len(full_data)}")
            return full_data
            
        except Exception as e:
            self.logger.error(f"编码失败: {str(e)}", exc_info=True)
            return b""
    
    def _parse_fields(self, data: bytes, fields: List[Dict[str, Any]], offset: int) -> Tuple[Dict[str, Any], int]:
        """解析字段列表
        
        Args:
            data: 原始数据
            fields: 字段配置列表
            offset: 起始偏移量
            
        Returns:
            (解析结果, 新的偏移量)
        """
        result = {}
        current_offset = offset
        
        for field in fields:
            if current_offset >= len(data):
                break
            
            field_name = field.get("name", "")
            field_length = field.get("length", 0)
            field_type = field.get("type", "hex")
            field_endian = field.get("endian", "big")
            
            if current_offset + field_length > len(data):
                self.logger.error(f"字段 {field_name} 数据不足: 需要 {field_length} 字节, 剩余 {len(data) - current_offset} 字节")
                break
            
            field_data = data[current_offset:current_offset + field_length]
            
            # 根据字段类型解析
            value = self._parse_field_value(field_data, field_type, field_endian)
            result[field_name] = value
            
            # 调试：打印解析的字段信息
            # self.logger.debug(f"解析字段 {field_name}: 原始数据={field_data.hex()}, 类型={field_type}, 字节序={field_endian}, 解析值={value}")
            
            current_offset += field_length
        
        return result, current_offset
    
    def _parse_field_value(self, data: bytes, field_type: str, endian: str) -> Any:
        """解析单个字段值
        
        Args:
            data: 字段数据
            field_type: 字段类型
            endian: 字节序
            
        Returns:
            解析后的值
        """
        if field_type == "hex":
            if endian == "little" and len(data) > 1:
                # 小端序字段，需要反转字节顺序
                # 例如：对于数据帧类型字段，将 '8B10' 转换为 '108B'
                return data[::-1].hex().upper()
            return data.hex().upper()
        elif field_type in ["int_le", "int_be"]:
            # 优先使用字段配置的endian，其次使用类型隐含的endian
            actual_endian = endian if endian in ["big", "little"] else ("little" if field_type == "int_le" else "big")
            return int.from_bytes(data, byteorder=actual_endian)
        elif field_type == "bcd":
            return self._bcd_to_str(data)
        elif field_type == "bit":
            return self._bit_to_list(data)
        elif field_type == "str":
            return data.decode("ascii", errors="ignore")
        else:
            return data.hex().upper()
    
    def _encode_field(self, field: Dict[str, Any], parsed_data: Dict[str, Any], response_data: Dict[str, Any]) -> bytes:
        """编码单个字段
        
        Args:
            field: 字段配置
            parsed_data: 解析后的数据
            response_data: 响应数据
            
        Returns:
            编码后的字段数据
        """
        field_name = field.get("name", "")
        field_length = field.get("length", 0)
        field_type = field.get("type", "hex")
        field_endian = field.get("endian", "big")
        field_value = field.get("value", "")
        
        # 处理 {pdu_left}_{field} 和 {pdu_left}.{field} 格式的字段名
        import re
        # 匹配 {pdu_left}_{field} 或 {pdu_left}.{field} 格式，其中 field 可以是任何字段名
        # 使用正则表达式匹配带花括号的字段名
        pdu_left_pattern = r'^\{pdu_left\}[\._](\w+)$'
        pdu_left_match = re.match(pdu_left_pattern, field_name)
        if pdu_left_match:
            # 提取实际字段名
            actual_field = pdu_left_match.group(1)
            # 从透传数据PDU中获取对应的值
            through_pdu = parsed_data.get("through_pdu", {})
            if actual_field in through_pdu:
                value = through_pdu[actual_field]
            else:
                value = field_value
        else:
            # 优先从响应数据中获取值
            if field_name in response_data:
                value = response_data[field_name]
            # 其次从解析数据中获取值（透传字段）
            elif field_name in parsed_data.get("through_sdu", {}):
                value = parsed_data["through_sdu"][field_name]
            # 最后使用默认值
            else:
                value = field_value
        
        # 评估时间函数
        value = self.time_utils.evaluate(value)
        
        # 处理占位符 {{data_frame_length}}
        if isinstance(value, str) and "{{data_frame_length}}" in value:
            # 获取数据帧类型
            data_frame_type = self._get_data_frame_type_from_parsed(parsed_data)
            # 查找对应的数据帧配置
            data_frame_config = self._get_data_frame_config(data_frame_type)
            # 获取data_frame_length值
            data_frame_length = str(data_frame_config.get("data_frame_length", 0))
            # 替换占位符
            value = value.replace("{{data_frame_length}}", data_frame_length)
        
        # 根据字段类型编码
        if field_type == "hex":
            if isinstance(value, str):
                # 处理空字符串
                if not value:
                    value = '00'
                # 移除可能的0x前缀
                if value.startswith('0x') or value.startswith('0X'):
                    value = value[2:]
                # 确保字符串长度为偶数
                if len(value) % 2 != 0:
                    value = '0' + value
                # 转换为字节
                data = bytes.fromhex(value.ljust(field_length * 2, '0')[:field_length * 2])
            elif isinstance(value, (int, float)):
                # 处理数字类型
                hex_str = f"{int(value):0{field_length * 2}X}"
                data = bytes.fromhex(hex_str)
            else:
                # 其他类型，使用默认值
                data = bytes.fromhex('00' * field_length)
            
            # 根据字节序调整
            if field_endian == "little" and field_length > 1:
                data = data[::-1]
        elif field_type in ["int_le", "int_be"]:
            # 优先使用字段配置的endian，其次使用类型隐含的endian
            actual_endian = field_endian if field_endian in ["big", "little"] else ("little" if field_type == "int_le" else "big")
            data = int(value).to_bytes(field_length, byteorder=actual_endian, signed=False)
        elif field_type == "bcd":
            data = self._str_to_bcd(str(value), field_length)
        elif field_type == "bit":
            data = self._list_to_bit(value, field_length)
        elif field_type == "str":
            data = str(value).encode("ascii").ljust(field_length, b'\x00')[:field_length]
        else:
            data = bytes([0] * field_length)
        
        return data
    
    def _generate_data_frame_type(self, pdu_left_result: Dict[str, Any], data_frame_result: Dict[str, Any]) -> str:
        """根据模板生成数据帧类型
        
        Args:
            pdu_left_result: PDU_LEFT解析结果
            data_frame_result: 数据帧解析结果
            
        Returns:
            生成的数据帧类型
        """
        if not self.data_frame_type_flag:
            return ""
        
        # 合并所有可能的字段
        all_fields = {**pdu_left_result, **data_frame_result}
        
        # 处理数组形式的data_frame_type_flag
        if isinstance(self.data_frame_type_flag, list):
            parts = []
            for field_name in self.data_frame_type_flag:
                if field_name in all_fields:
                    value = all_fields[field_name]
                    # 如果值是数字，转换为十六进制
                    if isinstance(value, int):
                        value = f"{value:02X}"
                    parts.append(str(value))
            return "".join(parts)
        # 兼容旧的字符串模板格式
        else:
            data_frame_type = self.data_frame_type_flag
            
            # 查找并替换所有 {field} 格式的占位符
            import re
            matches = re.findall(r'\{(\w+)\}', data_frame_type)
            for match in matches:
                if match in all_fields:
                    value = all_fields[match]
                    # 如果值是数字，转换为十六进制
                    if isinstance(value, int):
                        value = f"{value:02X}"
                    data_frame_type = data_frame_type.replace(f"{{{match}}}", str(value))
            
            return data_frame_type
    
    def _get_data_frame_type(self, pdu_left_result: Dict[str, Any], offset: int) -> str:
        """获取数据帧类型
        
        Args:
            pdu_left_result: PDU_LEFT解析结果
            offset: 数据帧偏移量
            
        Returns:
            数据帧类型
        """
        # 先从PDU_LEFT中查找
        if self.data_frame_type_flag in pdu_left_result:
            # 直接返回解析后的结果，字节序已经在解析阶段处理
            return pdu_left_result[self.data_frame_type_flag]
        
        # 默认为空
        return ""
    
    def _get_data_frame_type_from_parsed(self, parsed_data: Dict[str, Any]) -> str:
        """从解析结果中获取数据帧类型
        
        Args:
            parsed_data: 解析结果
            
        Returns:
            数据帧类型
        """
        # 处理列表类型的data_frame_type_flag
        if isinstance(self.data_frame_type_flag, list):
            # 合并所有可能的字段
            through_data = parsed_data.get("through_pdu", {})
            data_frame = parsed_data.get("through_sdu", {})
            all_fields = {**through_data, **data_frame}
            
            parts = []
            for field_name in self.data_frame_type_flag:
                if field_name in all_fields:
                    value = all_fields[field_name]
                    # 如果值是数字，转换为十六进制
                    if isinstance(value, int):
                        value = f"{value:02X}"
                    parts.append(str(value))
            return "".join(parts)
        # 兼容旧的字符串类型的data_frame_type_flag
        else:
            # 从透传数据PDU中查找
            through_data = parsed_data.get("through_pdu", {})
            if self.data_frame_type_flag in through_data:
                # 直接返回解析后的结果，字节序已经在解析阶段处理
                return through_data[self.data_frame_type_flag]
            
            # 从数据帧中查找
            data_frame = parsed_data.get("through_sdu", {})
            if self.data_frame_type_flag in data_frame:
                # 直接返回解析后的结果，字节序已经在解析阶段处理
                return data_frame[self.data_frame_type_flag]
        
        return ""
    
    def _get_data_frame_config(self, data_frame_type: str) -> Dict[str, Any]:
        """获取数据帧配置
        
        Args:
            data_frame_type: 数据帧类型（字符串或数组）
            
        Returns:
            数据帧配置
        """
        # 不做下划线兼容：
        # - 字符串类型：只做精确匹配
        # - 列表类型：只做精确匹配
        if isinstance(data_frame_type, str):
            target_parts = [data_frame_type]
        else:
            target_parts = data_frame_type

        for df in self.data_frame:
            df_type = df.get("data_frame_type")
            if not df_type:
                continue

            # 1) 优先按“原始分段”精确匹配（适合 df_type 为 list 或带下划线的 str）
            if isinstance(df_type, list):
                if df_type == target_parts:
                    return df
            else:
                # df_type is str
                if df_type == data_frame_type:
                    return df
        
        # 3. 对于传统的4字节类型，尝试反转字节顺序匹配（处理小端序问题）
        if isinstance(data_frame_type, str) and len(data_frame_type) == 4:
            reversed_type = data_frame_type[2:] + data_frame_type[:2]
            for df in self.data_frame:
                df_type = df.get("data_frame_type")
                if isinstance(df_type, str) and df_type == reversed_type:
                    return df
        
        # 4. 尝试直接匹配所有可能的数据帧类型
        for df in self.data_frame:
            if df.get("data_frame_type"):
                return df
        
        return {}
    
    def _calculate_checksum(self, data: bytes) -> bytes:
        """计算校验和
        
        Args:
            data: 数据
            
        Returns:
            包含校验和的数据
        """
        # 查找校验和字段
        checksum_field = None
        
        # 遍历pdu_tailer字段配置，找到checksum或check字段
        for field in self.pdu_tailer:
            field_name = field.get("name", "")
            if field_name in ("checksum", "check"):
                checksum_field = field
                break
        
        if not checksum_field:
            return data
        
        # 力维协议特殊处理
        if self.vendor_type == "liwei":
            # 力维协议：L.TH和CHK-SUM计算
            return self._calculate_liwei_checksum(data, checksum_field)
        
        # 获取校验和配置
        checksum_config = self.protocol_config.get("checksum_config", {})
        
        # 根据字段配置和checksum_config计算校验和
        field_length = checksum_field.get("length", 2)
        endian = checksum_field.get("endian", "little")
        
        # 计算校验和
        checksum = 0
        
        # 获取校验和算法配置
        algorithm = checksum_config.get("algorithm", "xor")
        start = checksum_config.get("start", 0)
        end = checksum_config.get("end", -field_length)
        
        # 根据配置计算校验和
        # 处理结束位置：如果是负数，表示从末尾开始计算
        if end < 0:
            end = len(data) + end
        else:
            end = min(end, len(data))
        
        # 确保start < end
        if start >= end or start >= len(data):
            # 无效的计算范围，使用默认值
            checksum = 0
        else:
            # 根据算法计算校验和
            if algorithm == "sum":
                # 求和算法
                checksum = sum(data[start:end])
            elif algorithm == "xor":
                # 异或算法
                checksum = 0
                for b in data[start:end]:
                    checksum ^= b
            elif algorithm == "sum_xor":
                # 先求和再异或
                checksum = sum(data[start:end])
                temp = checksum
                checksum = 0
                while temp > 0:
                    checksum ^= temp & 0xFF
                    temp >>= 8
            elif algorithm == "crc16":
                # CRC16算法实现
                crc = 0xFFFF
                for b in data[start:end]:
                    crc ^= b
                    for _ in range(8):
                        if crc & 0x0001:
                            crc = (crc >> 1) ^ 0xA001
                        else:
                            crc >>= 1
                checksum = crc & 0xFFFF
            else:
                # 默认使用异或算法
                checksum = 0
                for b in data[start:end]:
                    checksum ^= b
        
        # 根据字段长度限制校验和范围
        checksum &= (1 << (field_length * 8)) - 1
        
        # 构建完整的pdu_tailer
        new_pdu_tailer = bytearray()
        for field in self.pdu_tailer:
            field_name = field.get("name", "")
            field_len = field.get("length", 0)
            field_value = field.get("value", "00")
            
            if field_name in ("checksum", "check"):
                # 添加计算出的校验和
                new_pdu_tailer.extend(checksum.to_bytes(field_len, byteorder=endian, signed=False))
            elif field_name == "end":
                # 添加end字段（从模板获取）
                new_pdu_tailer.extend(bytes.fromhex(field_value))
            else:
                # 其他字段使用默认值或从原始数据复制
                # 对于固定长度的协议，我们直接使用默认值
                new_pdu_tailer.extend(bytes.fromhex(field_value * field_len))
        
        # 构建新的完整数据
        # 根据协议结构重新组装数据包
        if not self.dynamic_length and self.total_length > 0:
            # 固定长度协议：重新构建整个数据包
            # 提取pdu_left和data_frame部分
            # pdu_left的总长度
            pdu_left_length = 0
            for field in self.pdu_left:
                pdu_left_length += field.get("length", 0)
            
            # data_frame的总长度 = 总长度 - pdu_left长度 - pdu_tailer长度
            data_frame_length = self.total_length - pdu_left_length - len(new_pdu_tailer)
            
            # 提取pdu_left和data_frame数据
            pdu_left_data = data[:pdu_left_length]
            data_frame_data = data[pdu_left_length:pdu_left_length + data_frame_length]
            
            # 重新组装完整数据包
            new_data = bytearray()
            new_data.extend(pdu_left_data)
            new_data.extend(data_frame_data)
            new_data.extend(new_pdu_tailer)
            return bytes(new_data)
        else:
            # 动态长度协议：直接将pdu_tailer添加到数据末尾
            new_data = bytearray(data)
            new_data.extend(new_pdu_tailer)
            return bytes(new_data)
    
    def _calculate_liwei_checksum(self, data: bytes, checksum_field: Dict[str, Any]) -> bytes:
        """计算力维协议的校验和
        
        Args:
            data: 数据
            checksum_field: 校验和字段配置
            
        Returns:
            包含校验和的数据
        """
        # 力维协议结构：SOI(1) + VER(1) + ADR(1) + CID1(1) + CID2/RTN(1) + L.TH(2) + INFO(N) + CHK-SUM(2) + EOI(1)
        # 提取各个部分
        if len(data) < 9:  # 最小长度：1+1+1+1+1+2+2+1=9
            self.logger.error("{self.vendor}协议数据长度不足")
            return data
        
        soi = data[0:1]  # SOI: 7EH
        ver_adr_cid1_cid2 = data[1:5]  # VER(1) + ADR(1) + CID1(1) + CID2/RTN(1)
        
        # 优先使用保存的INFO数据（来自用户传入的response_data）
        if hasattr(self, '_liwei_info_data') and self._liwei_info_data:
            info = self._liwei_info_data
            self.logger.debug(f"使用保存的INFO数据: {info.hex().upper()}")
        else:
            info = data[7:-3]  # INFO部分：跳过前7字节（SOI+VER+ADR+CID1+CID2+L.TH），跳过最后3字节（CHK-SUM+EOI）
        
        eoi = bytes.fromhex("0D")  # EOI: 0DH，直接使用配置中定义的值
        
        # 1. 计算L.TH（参数长度校验）
        # 数据信息部分字节长度为L，ASCII码个数LENID=2L
        # 将LENID按4位分组，4组4位数累加后模16取补，作为LCHKSUM（高4位）
        L = len(info)  # INFO部分字节长度
        LENID = 2 * L  # ASCII码个数
        
        # 将LENID转换为4组4位数（高4位在前）
        lenid_bytes = LENID.to_bytes(2, byteorder='big')  # 2字节
        # 拆分每组4位数
        group1 = (lenid_bytes[0] >> 4) & 0x0F  # 第一组（最高4位）
        group2 = lenid_bytes[0] & 0x0F         # 第二组
        group3 = (lenid_bytes[1] >> 4) & 0x0F  # 第三组
        group4 = lenid_bytes[1] & 0x0F         # 第四组（最低4位）
        
        # 计算LCHKSUM：4组4位数累加后模16取补
        sum_groups = group1 + group2 + group3 + group4
        lchksum = (16 - (sum_groups % 16)) % 16
        
        # 构建L.TH：高8位是LENID的高8位 + LCHKSUM，低8位是LENID的低8位
        l_th_high = (group1 << 4) | lchksum
        l_th_low = lenid_bytes[1]
        l_th = bytes([l_th_high, l_th_low])
        
        # 2. 计算CHK-SUM（帧校验）
        # 从VER到INFO最后字节，按发送的ASCII码累加求和（双字节），模65536后取补运算
        # 注意：CHK-SUM是基于ASCII编码的十六进制字符串计算的
        # 构建需要计算CHK-SUM的数据部分：VER+ADR+CID1+CID2/RTN+L.TH+INFO
        chk_data = ver_adr_cid1_cid2 + l_th + info
        
        # 将二进制数据转换为ASCII编码的十六进制字符串
        ascii_hex = chk_data.hex().lower()
        
        # 计算ASCII码累加和
        chk_sum = sum(ord(c) for c in ascii_hex)
        
        # 模65536后取补运算
        chk_sum = (~chk_sum + 1) & 0xFFFF
        
        # 转换为字节
        chk_sum_bytes = chk_sum.to_bytes(2, byteorder='big')
        
        # 3. 构建完整的数据包
        full_data = soi + ver_adr_cid1_cid2 + l_th + info + chk_sum_bytes + eoi
        
        self.logger.debug(f"{self.vendor}协议校验和计算：")
        self.logger.debug(f"  INFO长度: {L} 字节")
        self.logger.debug(f"  LENID: {LENID} 字节")
        self.logger.debug(f"  L.TH: {l_th.hex().upper()}")
        self.logger.debug(f"  CHK-SUM计算数据: {chk_data.hex().upper()}")
        self.logger.debug(f"  CHK-SUM计算ASCII: {ascii_hex}")
        self.logger.debug(f"  CHK-SUM: {chk_sum_bytes.hex().upper()}")
        self.logger.debug(f"  完整数据包: {full_data.hex().upper()}")
        
        return full_data
    
    def _bcd_to_str(self, data: bytes) -> str:
        """BCD码转字符串
        
        Args:
            data: BCD数据
            
        Returns:
            字符串
        """
        result = ""
        for b in data:
            result += f"{b:02d}"
        return result
    
    def _str_to_bcd(self, s: str, length: int) -> bytes:
        """字符串转BCD码
        
        Args:
            s: 字符串
            length: 长度
            
        Returns:
            BCD数据
        """
        result = bytearray()
        s = s.ljust(length * 2, '0')[:length * 2]
        for i in range(0, len(s), 2):
            bcd_byte = int(s[i:i+2])
            result.append(bcd_byte)
        return bytes(result)
    
    def _bit_to_list(self, data: bytes) -> List[int]:
        """字节转位列表
        
        Args:
            data: 数据
            
        Returns:
            位列表
        """
        result = []
        for b in data:
            for i in range(8):
                result.append((b >> (7 - i)) & 0x01)
        return result
    
    def _list_to_bit(self, bit_list: List[int], length: int) -> bytes:
        """位列表转字节
        
        Args:
            bit_list: 位列表
            length: 长度
            
        Returns:
            数据
        """
        result = bytearray(length)
        bit_list = bit_list + [0] * (length * 8 - len(bit_list))
        
        for i, bit in enumerate(bit_list):
            byte_index = i // 8
            bit_index = 7 - (i % 8)
            result[byte_index] |= (bit & 0x01) << bit_index
        
        return bytes(result)
    
    def to_str(self, result: Dict[str, Any]) -> str:
        """将解析结果转换为字符串
        
        Args:
            result: 解析结果
            
        Returns:
            格式化的字符串
        """
        raw_data = result.get("raw_data", "")
        parsed = result.get("parsed", {})
        
        # 计算数据包长度字节数
        data_length = len(raw_data) // 2  # 每两个字符代表一个字节
        
        # 格式化原始HEX，每两个字符添加一个空格
        formatted_hex = ' '.join(raw_data[i:i+2] for i in range(0, len(raw_data), 2))
        lines = [f"[透传数据层]原始数据:", f"    数据包长度: {data_length} 字节", f"    HEX: {formatted_hex}", "[透传数据层] 协议栈解析:"]
        
        # 透传数据
        through_pdu = parsed.get("through_pdu", {})
        if through_pdu:
            lines.append("    透传数据PDU:")
            # 直接遍历through_pdu字典的键值对，使用字段名作为key
            for key, value in through_pdu.items():
                if value:
                    lines.append(f"        {key}: {value}")
        
        # 数据帧 - 单独处理，即使透传数据为空也能显示
        data_frame = parsed.get("through_sdu", {})
        if data_frame:
            lines.append("    透传数据帧:")
            for key, value in data_frame.items():
                lines.append(f"        {key}: {value}")
        
        return "\n".join(lines)
    
    def get_response_delay(self, rule_config: Dict[str, Any], performance_mode: bool) -> int:
        """获取响应延迟
        
        Args:
            rule_config: 规则配置
            performance_mode: 性能模式标志
            
        Returns:
            延迟时间（毫秒）
        """
        if performance_mode:
            return 0
        
        delay_ms = rule_config.get("delay_ms", 100)
        return random.randint(50, delay_ms)
