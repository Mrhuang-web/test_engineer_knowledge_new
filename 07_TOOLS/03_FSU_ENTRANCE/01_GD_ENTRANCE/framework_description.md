# FSU Mock Server 框架说明文档

## 1. 框架概述

FSU Mock Server 是一个用于模拟前端智能设备（FSU）的服务器框架，支持UDP和TCP协议，能够根据配置动态启动多个服务实例，用于测试和验证后端系统的设备管理功能。

### 主要功能
- 支持UDP和TCP协议
- 动态配置多实例服务
- 基于配置的协议解析和响应生成
- 支持多种设备厂商协议（邦讯、海能、亚奥、英嘉等）
- 灵活的规则配置系统
- 高性能异步IO设计
- 支持多进程部署

## 2. 代码层级逻辑思路解析

### 2.1 整体架构设计

FSU Mock Server 采用分层架构设计，各层职责明确，耦合度低，便于扩展和维护。整体架构分为以下几层：

| 层级 | 主要职责 | 核心文件 |
|------|----------|----------|
| 入口层 | 框架启动、配置加载、进程管理 | main.py |
| 配置管理层 | 配置文件加载和管理 | utils/config_manager.py |
| 服务器管理层 | UDP/TCP服务器启动和管理 | server/server_manager.py |
| 协议处理层 | 协议解析和响应生成 | server/base_protocol.py<br>server/udp_protocol.py<br>server/tcp_protocol.py |
| 编解码层 | 数据编码和解码 | codec/b_interface_codec.py<br>codec/through_data_codec.py |
| 工具层 | 日志、时间等通用工具 | utils/log_manager.py<br>utils/time_utils.py |

### 2.2 入口层（main.py）

**核心功能**：框架启动入口，负责加载配置、初始化日志、分配服务到进程等。

**关键逻辑流程**：
1. 加载系统配置 `sys_config.json`
2. 初始化日志管理器
3. 获取FSU服务列表
4. 根据CPU核心数分配FSU服务到不同进程
5. 每个进程启动相应的UDP或TCP服务器
6. 等待所有进程结束

**代码结构解析**：
- `run_fsu_services()`：运行一组FSU服务，创建异步任务
- `process_main()`：进程主函数，初始化日志并运行服务
- `main()`：主函数，负责加载配置、分配服务和创建进程

**设计思路**：
- 采用多进程架构，充分利用多核CPU
- 每个进程独立运行，避免相互影响
- 使用异步IO处理网络通信，提高性能

**维护建议**：
- 新增服务类型时，在 `run_fsu_services()` 中添加相应的服务启动逻辑
- 调整进程分配策略时，修改 `main()` 中的服务分配逻辑

### 2.3 配置管理层（utils/config_manager.py）

**核心功能**：负责加载和管理各种配置文件，包括系统配置、设备配置、协议模板和规则文件。

**关键逻辑流程**：
1. 加载系统配置：读取 `sys_config.json`
2. 加载设备配置：读取 `fsu_devices.json`
3. 加载协议模板：读取厂商特定的协议模板文件
4. 加载规则文件：优先加载FSU特定规则，其次加载默认规则

**代码结构解析**：
- `FSUConfig`：管理系统配置
  - `_load_config()`：加载系统配置文件
  - `get_log_config()`：获取日志配置
  - `get_performance_config()`：获取性能配置
  - `get_fsu_list()`：获取FSU服务列表
- `DeviceConfig`：管理设备配置
  - `_load_devices()`：加载设备配置
  - `load_protocol_template()`：加载协议模板
  - `load_rules_with_separate_objects()`：加载规则文件
  - `match_rule_by_data_frame_type()`：根据数据帧类型匹配规则

**设计思路**：
- 配置与代码分离，便于动态调整
- 支持分层配置，提高配置复用性
- 支持规则优先级，便于个性化配置

**维护建议**：
- 新增配置项时，在相应的配置类中添加获取方法
- 修改配置加载逻辑时，注意保持向后兼容
- 规则文件加载逻辑复杂，修改时需仔细测试

### 2.4 服务器管理层（server/server_manager.py）

**核心功能**：负责启动和管理UDP和TCP服务器，协调协议处理和数据通信。

**关键逻辑流程**：
1. `run_udp_server()`：启动UDP服务器
   - 创建B接口编解码器
   - 创建UDP协议实例
   - 启动UDP服务器
   - 启动心跳发送任务
2. `run_tcp_server()`：启动TCP服务器
   - 创建TCP协议实例
   - 启动TCP服务器
3. `heartbeat_task()`：心跳发送任务
   - 定期发送心跳包

**代码结构解析**：
- 两个核心函数：`run_udp_server()` 和 `run_tcp_server()`
- 一个辅助函数：`heartbeat_task()`

**设计思路**：
- 统一的服务器启动接口，便于扩展新的协议类型
- 心跳机制确保连接可靠性
- 异步IO设计，提高并发处理能力

**维护建议**：
- 新增协议类型时，添加相应的服务器启动函数
- 修改心跳机制时，注意保持兼容性
- 服务器配置调整时，确保所有相关参数同步更新

### 2.5 协议处理层

#### 2.5.1 基础协议类（server/base_protocol.py）

**核心功能**：定义TCP和UDP协议共用的方法，如协议加载、响应生成等。

**关键逻辑流程**：
1. `load_protocols()`：加载设备协议模板和规则
2. `_generate_response()`：生成响应数据
3. `_extract_actual_type()`：提取真正的命令类型

**代码结构解析**：
- `load_protocols()`：加载所有设备的协议模板和规则
- `_generate_response()`：根据数据帧类型匹配规则，生成响应
- `_extract_actual_type()`：处理不同格式的数据帧类型

**设计思路**：
- 抽象出共用逻辑，减少代码重复
- 支持多种数据帧类型识别方式
- 灵活的规则匹配机制

**维护建议**：
- 新增协议类型时，确保 `load_protocols()` 能正确加载
- 修改响应生成逻辑时，注意保持兼容性
- 数据帧类型识别逻辑复杂，修改时需仔细测试

#### 2.5.2 UDP协议类（server/udp_protocol.py）

**核心功能**：处理UDP协议通信，包括B接口解码、透传数据处理、响应编码等。

**关键逻辑流程**：
1. `connection_made()`：建立连接时调用，初始化传输对象
2. `datagram_received()`：收到UDP数据包时调用
   - 保存SC地址
   - 解码B接口数据
   - 创建任务处理透传数据
3. `_handle_through_data()`：处理透传数据
   - 解码透传数据
   - 生成响应数据
   - 编码响应数据
   - 编码B接口响应
   - 发送响应
4. `send_heartbeat()`：发送心跳包

**代码结构解析**：
- 继承自 `BaseProtocol` 和 `asyncio.DatagramProtocol`
- 实现UDP协议的核心方法
- 使用异步任务处理数据

**设计思路**：
- 遵循异步IO设计模式
- 分离数据接收和处理逻辑，提高并发性能
- 完整的日志记录，便于调试

**维护建议**：
- 修改B接口处理逻辑时，注意保持与编解码器的一致性
- 新增UDP特定功能时，在该类中添加相应方法
- 调试UDP通信问题时，重点查看该类的日志

#### 2.5.3 TCP协议类（server/tcp_protocol.py）

**核心功能**：处理TCP协议通信，包括数据接收、透传数据处理、响应编码等。

**关键逻辑流程**：
1. `connection_made()`：建立连接时调用，初始化传输对象
2. `data_received()`：收到TCP数据时调用
   - 创建任务处理TCP数据
3. `_handle_tcp_data()`：处理TCP数据
   - 解码透传数据
   - 生成响应数据
   - 编码响应数据
   - 发送响应
4. `connection_lost()`：连接关闭时调用

**代码结构解析**：
- 继承自 `BaseProtocol` 和 `asyncio.Protocol`
- 实现TCP协议的核心方法
- 使用异步任务处理数据

**设计思路**：
- 遵循异步IO设计模式
- 简化TCP处理逻辑，直接处理透传数据
- 完整的日志记录，便于调试

**维护建议**：
- 修改TCP处理逻辑时，注意保持与透传编解码器的一致性
- 新增TCP特定功能时，在该类中添加相应方法
- 调试TCP通信问题时，重点查看该类的日志

### 2.6 编解码层

#### 2.6.1 B接口编解码器（codec/b_interface_codec.py）

**核心功能**：处理UDP外层协议的编码和解码，包括B接口的封装和解析。

**关键逻辑流程**：
1. `decode()`：解码B接口数据
   - 检查包头和包尾
   - 反转义数据
   - 计算校验和
   - 解析负载数据
2. `encode()`：编码B接口数据
   - 构建负载数据
   - 计算校验和
   - 转义数据
   - 添加包头和包尾
3. `_calculate_checksum()`：计算校验和
4. `_parse_payload()`：解析负载数据
5. `_build_payload()`：构建负载数据

**代码结构解析**：
- 实现B接口的完整编解码逻辑
- 支持数据转义和反转义
- 支持校验和计算

**设计思路**：
- 严格遵循B接口协议规范
- 完整的错误处理
- 支持多种命令类型

**维护建议**：
- 修改B接口协议时，需同步更新编解码逻辑
- 新增命令类型时，在 `_parse_payload()` 和 `_build_payload()` 中添加相应处理
- 校验和算法修改时，需仔细测试

#### 2.6.2 透传数据编解码器（codec/through_data_codec.py）

**核心功能**：处理不同厂商的透传数据编码和解码，包括协议解析、响应生成和校验和计算。

**关键逻辑流程**：
1. `decode()`：解码透传数据
   - 验证数据长度
   - 解析协议头（PDU_LEFT）
   - 解析数据帧（DATA_FRAME）
   - 解析协议尾（PDU_TAILER）
2. `encode()`：编码透传数据
   - 编码数据帧
   - 编码协议头
   - 编码协议尾
   - 计算校验和
3. `_parse_fields()`：解析字段列表
4. `_encode_field()`：编码单个字段
5. `_generate_data_frame_type()`：生成数据帧类型
6. `_calculate_checksum()`：计算校验和

**代码结构解析**：
- 支持多种字段类型：hex、int_le、int_be、bcd、bit、str
- 支持不同字节序：big、little
- 支持动态数据帧类型生成
- 支持厂商特定校验和算法

**设计思路**：
- 模块化设计，支持多种厂商协议
- 配置驱动，便于扩展新协议
- 灵活的字段处理机制

**维护建议**：
- 新增厂商协议时，在 `_calculate_checksum()` 中添加相应的校验和算法
- 新增字段类型时，在 `_parse_field_value()` 和 `_encode_field()` 中添加相应处理
- 数据帧类型生成逻辑复杂，修改时需仔细测试

### 2.7 工具层

#### 2.7.1 日志管理器（utils/log_manager.py）

**核心功能**：管理日志记录，支持多设备日志、异步写入和日志轮转。

**关键逻辑流程**：
1. 初始化日志配置
2. 创建日志文件处理器
3. 设置日志级别和格式
4. 支持多设备日志隔离
5. 支持异步日志写入

**代码结构解析**：
- 单例模式设计，确保日志配置唯一
- 支持多设备日志，便于调试
- 支持异步写入，提高性能

**设计思路**：
- 灵活的日志配置
- 高性能日志写入
- 便于调试和监控

**维护建议**：
- 新增日志类型时，添加相应的日志获取方法
- 调整日志格式时，修改相应的格式字符串
- 性能优化时，考虑启用异步日志写入

#### 2.7.2 时间工具（utils/time_utils.py）

**核心功能**：提供时间相关的工具函数，支持动态生成时间字段。

**关键逻辑流程**：
1. 解析时间函数表达式
2. 生成相应的时间字段值
3. 支持多种时间格式

**代码结构解析**：
- `evaluate()`：评估时间函数表达式
- 支持的函数：year、month、day、week、hour、minute、second

**设计思路**：
- 灵活的时间函数表达式
- 支持多种时间格式
- 便于动态生成响应数据

**维护建议**：
- 新增时间函数时，在 `evaluate()` 中添加相应的处理逻辑
- 修改时间格式时，注意保持兼容性

### 2.8 各层交互关系

**整体交互流程**：
1. 入口层启动服务器，加载配置
2. 配置管理层提供各种配置信息
3. 服务器管理层启动相应的服务器
4. 协议处理层处理网络通信和协议逻辑
5. 编解码层负责数据的编码和解码
6. 工具层提供日志和时间等通用功能

**数据流向**：
- 接收数据：网络 → 服务器层 → 编解码层 → 协议处理层 → 生成响应
- 发送数据：协议处理层 → 编解码层 → 服务器层 → 网络

**调用关系**：
- 入口层调用配置管理层和服务器管理层
- 服务器管理层调用协议处理层
- 协议处理层调用编解码层和配置管理层
- 编解码层调用工具层

### 2.9 代码扩展建议

1. **新增厂商协议**：
   - 创建新的厂商配置目录
   - 编写协议模板和规则文件
   - 如需特殊处理，修改编解码层相应逻辑

2. **新增服务类型**：
   - 在服务器管理层添加新的服务启动函数
   - 在入口层添加相应的服务启动逻辑

3. **新增字段类型**：
   - 在透传数据编解码器中添加新的字段类型处理

4. **新增时间函数**：
   - 在时间工具中添加新的时间函数处理逻辑

5. **性能优化**：
   - 优化日志写入机制
   - 调整进程分配策略
   - 优化协议解析逻辑

### 2.10 新手快速上手指南

1. **理解框架结构**：先阅读文档，了解框架的层级结构和各层功能
2. **查看示例配置**：研究现有厂商的配置文件，了解配置格式
3. **调试日志**：启用debug级别日志，查看详细的处理流程
4. **从简单开始**：先尝试修改现有配置，再尝试新增协议
5. **测试验证**：使用测试工具发送请求，验证响应是否符合预期
6. **逐步扩展**：从简单功能开始，逐步扩展到复杂功能

通过理解框架的层级结构和每层的逻辑思路，新手可以快速上手，高效地维护和扩展框架功能。

## 3. 目录结构

```
fsu_b_mock/
├── codec/                 # 编解码器模块
│   ├── b_interface_codec.py   # B接口编解码器（UDP外层协议）
│   └── through_data_codec.py  # 透传数据编解码器
├── config/                # 配置文件目录
│   ├── sys_config.json        # 系统配置
│   ├── vendor.json            # 厂商配置
│   ├── bangsun_new/           # 邦讯新版配置
│   ├── bangsun_old/           # 邦讯旧版配置
│   ├── haineng_01/            # 海能配置
│   ├── jiangsuyao_01/         # 江苏亚奥配置
│   ├── yingjia/               # 英嘉配置
│   └── UDP-ES1000/            # ES1000配置
├── server/                # 服务器模块
│   ├── __init__.py
│   ├── base_protocol.py       # 基础协议类
│   ├── server_manager.py      # 服务器管理器
│   ├── tcp_protocol.py        # TCP协议实现
│   └── udp_protocol.py        # UDP协议实现
├── utils/                 # 工具模块
│   ├── config_manager.py      # 配置管理器
│   ├── log_manager.py         # 日志管理器
│   └── time_utils.py          # 时间工具
├── main.py                # 主程序入口
├── start.sh               # 启动脚本
└── test_*.py              # 测试脚本
```

## 3. 核心组件

### 3.1 配置管理

- **FSUConfig**: 管理系统配置，包括日志配置、性能配置和FSU服务列表
- **DeviceConfig**: 管理设备配置，包括设备列表、协议模板和规则文件

### 3.2 服务器管理

- **ServerManager**: 负责启动和管理UDP和TCP服务器
- **BaseProtocol**: 基础协议类，包含TCP和UDP共用的方法
- **UDPProtocol**: UDP协议实现，处理B接口通信
- **TCPProtocol**: TCP协议实现，直接处理透传数据

### 3.3 编解码

- **BInterfaceCodec**: B接口编解码器，处理UDP外层协议封装和解析
- **ThroughDataCodec**: 透传数据编解码器，处理不同厂商的具体协议

### 3.4 工具类

- **LogManager**: 日志管理，支持多设备日志和异步写入
- **TimeFunctionUtils**: 时间函数工具，支持动态生成时间相关字段

## 4. 配置项说明

### 4.1 系统配置（sys_config.json）

```json
{
    "log": {
        "level": "debug",           // 日志级别：debug, info, warn, error
        "dir": "./logs",           // 日志目录
        "maxSize": 1024000,         // 日志文件最大大小（字节）
        "maxAge": 7,                // 日志保留天数
        "async_write": false,       // 是否异步写入
        "file": "system_%Y%m%d.log" // 日志文件名格式
    },
    "performance": {
        "enabled": false,           // 是否启用性能模式
        "skip_delay": true,         // 是否跳过响应延迟
        "skip_device_log": true     // 是否跳过设备日志
    },
    "fsu_list": [                  // FSU服务列表
        {
            "fsuname": "bangsun_01",    // FSU名称
            "fsuid": "313234313233313331323431",  // FSU ID
            "desc": "描述",              // 描述信息
            "port": 10101,              // 监听端口
            "host": "0.0.0.0",         // 监听地址
            "protocol_type": "udp",    // 协议类型：udp或tcp
            "heartbeat_interval": 120,  // 心跳间隔（秒）
            "config_dir": "./config/bangsun_old"  // 配置目录
        }
    ]
}
```

### 4.2 设备配置（fsu_devices.json）

```json
{
    "device_list": [
        {
            "vendor": "邦讯-旧版",            // 厂商名称
            "sub_dev_type": "01",             // 子设备类型
            "sub_dev_addr": "01",             // 子设备地址
            "protocol_template": "./bangsun_old.json"  // 协议模板路径
        }
    ]
}
```

### 4.3 协议模板（xxx.json）

```json
{
    "vendor": "邦讯-旧版",            // 厂商名称
    "rule_file_list": [               // 规则文件列表
        "./rules/0101.json",
        "./rules/313234313233313331323431.json"
    ],
    "protocol": {
        "dynamic_length": false,      // 是否动态长度
        "total_length": 34,           // 固定总长度
        "pdu_left": [                 // 协议头字段
            {
                "name": "start",     // 字段名
                "length": 1,          // 字段长度
                "type": "hex",       // 字段类型
                "value": "7E"        // 字段默认值
            }
        ],
        "pdu_tailer": [               // 协议尾字段
            {
                "name": "checksum",  // 校验和
                "length": 2,
                "endian": "little",  // 字节序
                "type": "hex"
            }
        ],
        "data_frame_type_flag": "data_frame_type",  // 数据帧类型标志
        "data_frame": [               // 数据帧配置
            {
                "data_frame_type": "109D",  // 数据帧类型
                "align": "left",     // 对齐方式
                "padding": "00",     // 填充字节
                "req_data_list": [    // 请求数据字段列表
                    {
                        "name": "data_frame_type",
                        "length": 2,
                        "endian": "little",
                        "type": "hex"
                    }
                ],
                "resp_data_list": [   // 响应数据字段列表
                    {
                        "name": "data_frame_type",
                        "length": 2,
                        "endian": "little",
                        "type": "hex",
                        "value": "109D"
                    }
                ]
            }
        ]
    }
}
```

### 4.4 规则文件（rules/*.json）

```json
{
    "108B": {                  // 数据帧类型
        "delay_ms": 100,       // 响应延迟（毫秒）
        "data": {              // 响应数据
            "year": "${year(yy)}$",  // 动态时间字段
            "month": "${month()}$",
            "day": "${day()}$"
        }
    }
}
```

## 5. 框架使用方式

### 5.1 启动服务

```bash
python main.py
```

### 5.2 配置新设备

1. 在 `config` 目录下创建新的设备配置目录
2. 创建 `fsu_devices.json` 文件，配置设备列表
3. 创建协议模板文件（如 `new_vendor.json`）
4. 创建规则文件目录 `rules`，并添加规则文件
5. 在 `sys_config.json` 中添加新的FSU服务配置

### 5.3 配置规则

规则文件支持动态生成响应数据，使用 `${function()}` 格式的函数调用：

- `${year()}`: 生成完整年份（如2023）
- `${year(yy)}`: 生成两位年份（如23）
- `${month()}`: 生成月份（01-12）
- `${day()}`: 生成日期（01-31）
- `${week()}`: 生成星期（01-07）
- `${hour()}`: 生成小时（00-23）
- `${minute()}`: 生成分钟（00-59）
- `${second()}`: 生成秒（00-59）

## 6. 框架逻辑流程

### 6.1 启动流程

1. 加载系统配置 `sys_config.json`
2. 初始化日志管理器
3. 获取FSU服务列表
4. 根据CPU核心数分配FSU服务到不同进程
5. 每个进程启动相应的UDP或TCP服务器
6. UDP服务器启动心跳发送任务

### 6.2 数据处理流程

#### UDP协议

1. 收到UDP数据包
2. 保存SC（服务器中心）地址
3. 解码B接口数据，得到透传数据
4. 根据设备协议模板解码透传数据
5. 生成响应数据
6. 编码响应数据
7. 添加延迟（如果不是性能模式）
8. 编码B接口响应
9. 发送响应到SC

#### TCP协议

1. 收到TCP数据
2. 直接解码透传数据
3. 生成响应数据
4. 编码响应数据
5. 添加延迟（如果不是性能模式）
6. 发送响应到客户端

### 6.3 响应生成流程

1. 根据解析得到的数据帧类型，查找对应的规则
2. 评估规则中的动态函数（如时间函数）
3. 生成响应数据
4. 根据协议模板编码响应数据
5. 计算校验和
6. 返回完整的响应数据包

## 7. 透传结构

透传结构是指在B接口（UDP）或直接在TCP中传输的具体设备协议数据，不同厂商有不同的透传结构。

### 7.1 透传结构组成

```
透传数据 = PDU_LEFT + DATA_FRAME + PDU_TAILER
```

- **PDU_LEFT**: 协议头，包含起始标志、地址等信息
- **DATA_FRAME**: 数据帧，包含具体的命令和数据
- **PDU_TAILER**: 协议尾，包含校验和、结束标志等信息

### 7.2 字段定义

- **name**: 字段名，用于标识字段
- **length**: 字段长度，单位为字节
- **type**: 字段类型，包括hex（十六进制）、int_le（小端整数）、int_be（大端整数）、bcd（BCD码）、bit（位）、str（字符串）
- **endian**: 字节序，包括big（大端）、little（小端）
- **value**: 字段默认值

### 7.3 数据帧类型

数据帧类型用于标识不同的命令，通过 `data_frame_type_flag` 配置来确定如何从数据中提取数据帧类型：

- 字符串格式：如 `"data_frame_type_flag": "data_frame_type"`
- 数组格式：如 `"data_frame_type_flag": ["field1", "field2"]`
- 模板格式：如 `"data_frame_type_flag": "{field1}_{field2}"`

## 8. B接口外层结构

B接口是UDP协议的外层封装，用于FSU和SC之间的通信。

### 8.1 B接口结构

```
B接口数据包 = P_HEADER + ESCAPED_DATA + P_TAILER
```

- **P_HEADER**: 包头，固定为0xFF
- **ESCAPED_DATA**: 转义后的数据，包含地址、命令类型、透传数据等
- **P_TAILER**: 包尾，固定为0xFE

### 8.2 转义规则

| 原始字节 | 转义后 |
|----------|--------|
| 0xFF     | 0xFD 0x00 |
| 0xFE     | 0xFD 0x01 |
| 0xFD     | 0xFD 0x02 |

### 8.3 负载数据结构

```
负载数据 = P_dest_addr + P_src_addr + P_subDevType + P_subDev_addr + P_pLen + RtnFlag + CommType + through_data_len + through_data
```

- **P_dest_addr**: 目标地址，8字节，SC地址
- **P_src_addr**: 源地址，20字节，FSU ID
- **P_subDevType**: 子设备类型，1字节
- **P_subDev_addr**: 子设备地址，1字节
- **P_pLen**: 协议族数据包长度
- **RtnFlag**: 返回标志
- **CommType**: 命令类型
  - 0x0001: 普通命令
  - 0x0002: 心跳命令
- **through_data_len**: 透传数据长度
- **through_data**: 透传数据

### 8.4 校验和

B接口使用异或校验，计算范围为转义前的数据（不包括包头和包尾）。

## 9. 性能优化

- **异步IO**: 使用asyncio实现高性能异步IO
- **多进程**: 根据CPU核心数分配服务实例，充分利用多核CPU
- **性能模式**: 支持跳过延迟和日志，提高性能
- **动态规则加载**: 支持根据FSU ID动态加载规则，提高匹配效率

## 10. 测试与调试

- 提供多种测试脚本，如 `test_bangsun.py`、`test_haineng.py` 等
- 支持详细的日志输出，便于调试
- 支持动态修改规则文件，无需重启服务

## 11. 扩展建议

- 支持更多厂商协议
- 增加Web管理界面
- 支持动态添加和删除服务
- 增加统计和监控功能
- 支持更多的动态函数

## 13. 新增协议详细流程

### 12.1 手动新增协议

#### 12.1.1 配置文件创建与修改

1. **创建厂商配置目录**
   - 路径：`config/new_vendor/`
   - 命名规则：小写字母+下划线，如 `new_vendor/`

2. **创建设备配置文件**
   - 文件名：`config/new_vendor/fsu_devices.json`
   - 内容示例：
   ```json
   {
       "device_list": [
           {
               "vendor": "新厂商",      // 厂商名称，需与协议模板中的vendor一致
               "sub_dev_type": "01",   // 子设备类型，十六进制字符串
               "sub_dev_addr": "01",   // 子设备地址，十六进制字符串
               "protocol_template": "./new_vendor.json"  // 协议模板相对路径
           }
       ]
   }
   ```

3. **创建协议模板文件**
   - 文件名：`config/new_vendor/new_vendor.json`
   - 核心配置项说明：
     - `vendor`：厂商名称，用于标识不同厂商的协议
     - `rule_file_list`：规则文件列表，支持多个规则文件叠加
     - `protocol`：协议结构定义
       - `dynamic_length`：是否动态长度
       - `total_length`：固定总长度（仅动态长度为false时有效）
       - `pdu_left`：协议头字段列表
       - `pdu_tailer`：协议尾字段列表
       - `data_frame_type_flag`：数据帧类型标识字段
       - `data_frame`：数据帧配置列表
   - 字段配置示例：
   ```json
   {
       "name": "data_frame_type",  // 字段名
       "length": 2,                 // 字段长度（字节）
       "type": "hex",              // 字段类型：hex/int_le/int_be/bcd/bit/str
       "endian": "little",         // 字节序：big/little
       "value": "109D"             // 字段默认值
   }
   ```

4. **创建规则文件**
   - 目录：`config/new_vendor/rules/`
   - 默认规则文件：`default.json`（必须）
   - FSU特定规则文件：`{fsuid}.json`（可选，优先级高于default）
   - 规则配置示例：
   ```json
   {
       "109D": {                     // 数据帧类型，与协议模板中data_frame_type对应
           "delay_ms": 100,          // 响应延迟（毫秒）
           "data": {                 // 响应数据，字段与resp_data_list对应
               "first": "00"        // 字段名与值
           }
       }
   }
   ```

5. **配置系统服务**
   - 文件名：`config/sys_config.json`
   - 配置项位置：`fsu_list` 数组中添加新对象
   - 配置示例：
   ```json
   {
       "fsuname": "new_vendor_01",  // FSU名称，唯一标识
       "fsuid": "313234313233313331323431",  // FSU ID，十六进制字符串
       "desc": "新厂商设备模拟",      // 描述信息
       "port": 10200,               // 监听端口，确保不冲突
       "host": "0.0.0.0",          // 监听地址，0.0.0.0表示所有网卡
       "protocol_type": "udp",     // 协议类型：udp/tcp
       "heartbeat_interval": 120,   // 心跳间隔（秒），仅UDP有效
       "config_dir": "./config/new_vendor"  // 配置目录相对路径
   }
   ```

#### 12.1.2 代码修改点

1. **协议解析特殊逻辑**
   - 文件：`codec/through_data_codec.py`
   - 修改点：`decode()` 方法，添加新厂商的特殊解析逻辑
   - 示例：
   ```python
   # 在decode方法中添加
   if self.vendor == "新厂商":
       # 新厂商特殊解析逻辑
       pass
   ```

2. **厂商特定数据帧类型处理**
   - 文件：`server/base_protocol.py`
   - 修改点：`_generate_response()` 方法，添加厂商特定的数据帧类型处理
   - 示例：
   ```python
   # 在_generate_response方法中添加
   if vendor == "新厂商":
       # 新厂商特殊数据帧类型处理
       actual_type = f"{cid1}{actual_type}"
   ```

3. **校验和计算**
   - 文件：`codec/through_data_codec.py`
   - 修改点：`_calculate_checksum()` 方法，添加新厂商的校验和算法
   - 示例：
   ```python
   # 在_calculate_checksum方法中添加
   elif self.vendor == "新厂商":
       # 新厂商校验和算法
       checksum = 0
       for b in data[:-field_length]:
           checksum += b
       checksum &= 0xFFFF
   ```

### 12.2 通过AI生成协议

#### 12.2.1 准备工作

1. **收集协议文档**
   - 要求：包含完整的协议结构、字段定义、数据类型、字节序和示例
   - 格式：PDF或Word文档均可

2. **转化为MD格式**
   - 工具：使用在线转换工具或手动编写
   - 存放目录：`md/`
   - 命名规则：`vendor_name.md`，如 `new_vendor.md`
   - 核心结构要求：
     - 协议概述
     - 帧结构定义
     - 字段详细说明
     - 命令类型列表
     - 示例数据包
   - MD模板示例：
   ```markdown
   # 新厂商协议

   ## 1. 协议概述
   新厂商门禁设备通信协议，基于UDP/TCP，采用二进制格式。

   ## 2. 帧结构
   ```
   帧结构 = 起始标志(1B) + 地址(2B) + 命令类型(2B) + 数据长度(2B) + 数据(NB) + 校验和(2B) + 结束标志(1B)
   ```

   ## 3. 字段说明
   | 字段名 | 长度 | 类型 | 说明 |
   |--------|------|------|------|
   | 起始标志 | 1B | 固定值 | 0x7E |
   | 地址 | 2B | 十六进制 | 设备地址 |
   ```
   ```

3. **使用Trae工具生成配置**
   - 安装：`pip install trae`
   - 执行命令：
   ```bash
   trae parse md/new_vendor.md --output config/new_vendor/
   ```
   - 输出：自动生成协议模板和规则文件

#### 12.2.2 生成后验证与调整

1. **检查生成结果**
   - 验证文件：`config/new_vendor/new_vendor.json` 和 `config/new_vendor/rules/default.json`
   - 重点检查：
     - 字段长度、类型、字节序是否正确
     - 数据帧类型配置是否完整
     - 规则文件是否包含所有命令类型

2. **测试验证**
   - 配置系统服务：在 `sys_config.json` 中添加测试服务
   - 启动服务：`python main.py`
   - 发送测试请求：使用socket工具发送符合协议的请求数据包
   - 验证响应：检查响应数据包是否符合预期

3. **调整优化**
   - 根据测试结果调整协议模板中的字段配置
   - 补充缺失的规则配置
   - 优化动态字段的处理

## 14. 配置项最佳实践

### 13.1 系统配置

| 环境 | 日志级别 | 性能模式 | 说明 |
|------|----------|----------|------|
| 开发 | debug | false | 详细日志，便于调试 |
| 测试 | info | false | 基本日志，记录关键信息 |
| 生产 | warn | true | 仅记录警告和错误，跳过延迟 |

### 13.2 协议模板

1. **字段配置**
   - 优先使用 `hex` 类型处理二进制数据
   - 明确指定 `endian`（字节序），避免默认值导致的问题
   - 固定长度字段必须指定 `length`

2. **数据帧类型**
   - 使用 `data_frame_type_flag` 准确标识命令类型
   - 支持复合类型，如 `["field1", "field2"]` 生成 `field1_field2` 作为数据帧类型

3. **校验和**
   - 明确校验和计算范围和算法
   - 校验和字段必须放在 `pdu_tailer` 中

### 13.3 规则文件

1. **动态函数使用**
   - 时间相关字段使用内置函数：`${year(yy)}$`、`${month()}$` 等
   - 支持的函数：`year`/`month`/`day`/`week`/`hour`/`minute`/`second`

2. **延迟配置**
   - 根据设备实际响应时间设置合理的 `delay_ms`
   - 性能模式下 `delay_ms` 会被忽略

## 15. 常见问题与解决方案

### 14.1 协议解析失败
- **原因**：字段长度配置错误、字节序错误、数据类型错误
- **解决方案**：
  1. 检查协议模板中的字段长度与实际协议是否一致
  2. 验证字节序配置是否正确
  3. 查看日志中的详细错误信息

### 14.2 找不到数据帧类型
- **原因**：`data_frame_type_flag` 配置错误、数据帧类型不匹配
- **解决方案**：
  1. 检查 `data_frame_type_flag` 是否指向正确的字段
  2. 验证数据帧类型格式是否与规则文件中的键一致
  3. 查看日志中的数据帧类型生成信息

### 14.3 校验和错误
- **原因**：校验和算法配置错误、计算范围错误
- **解决方案**：
  1. 确认厂商提供的校验和算法
  2. 在 `_calculate_checksum` 方法中添加正确的算法实现

### 14.4 响应数据不符合预期
- **原因**：规则配置错误、字段映射错误
- **解决方案**：
  1. 检查规则文件中的字段名与协议模板中的 `resp_data_list` 是否一致
  2. 验证规则中的字段值格式是否正确
  3. 查看日志中的响应生成信息

## 16. 性能优化建议

1. **服务部署**
   - 生产环境建议使用多进程部署，充分利用CPU核心
   - 每个进程管理的服务数量不宜过多，建议每个进程管理5-10个服务

2. **日志配置**
   - 生产环境使用 `warn` 级别日志
   - 启用 `async_write` 异步写入，提高性能

3. **规则管理**
   - 避免过多规则文件叠加，建议每个厂商使用2-3个规则文件
   - 合理组织规则，将频繁使用的规则放在优先级高的文件中

4. **协议设计**
   - 固定长度协议比动态长度协议处理效率更高
   - 简化协议结构，减少不必要的字段

5. **网络优化**
   - UDP协议建议启用心跳机制，及时检测连接状态
   - TCP协议建议设置合理的超时时间

通过以上详细流程和最佳实践，您可以高效地新增和维护各种厂商的协议配置，确保FSU Mock Server能够准确模拟各种设备的行为，满足测试需求。