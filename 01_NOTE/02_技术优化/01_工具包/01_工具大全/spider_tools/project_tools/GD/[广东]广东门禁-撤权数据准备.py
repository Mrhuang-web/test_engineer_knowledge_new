# [广东]广东门禁-撤权数据准备.py
import os
import re
import time

# 导入基础模块
import requests
import spider_tools.Common.TestEnv as TestEnv
from asptest.common.mysqlpool import MySQLHelper
from spider_tools.Common.Utils import get_need_uuid4

# 定义全局数据库连接对象，将在main函数中初始化
conn_obj = None


def generate_card_numbers():
    # 定义固定的卡号枚举值，确保每次运行结果一致
    fixed_card_numbers = {
        "1": ["1234567890", "987654321", "1000000000"],  # 十进制，10位以内
        "2": ["ABC1234567", "DEF8901234", "123456789A"],  # 十六进制，10位以内
        "7": ["1000000000", "2000000000", "3000000000"],  # 未指定格式，默认10位
        "3": ["1234567", "89012345", "10000000"],  # 十进制，8位以内
        "4": ["1111111111", "2222222222", "3333333333"],  # 未指定格式，默认10位
        "5": ["ABC12340", "DEF56780", "12345670"],  # 十六进制，8位，末尾补0
        "6": ["ABCDEF1234", "1234ABCDEF", "DEF1234ABC"],  # 十六进制，10位以内
        "8": ["4444444444", "5555555555", "6666666666"],  # 未指定格式，默认10位
        "13": ["7777777777", "8000000000", "9000000000"],  # 未指定格式，默认10位
        "12": ["ABC9A0", "DEFCD0", "123890"],  # 十六进制，6位，末尾补0
        "14": ["7878787878", "9090909090", "1313131313"],  # 未指定格式，默认10位
        "15": ["5757575757", "2424242424", "8989898989"],  # 未指定格式，默认10位
        "16": ["ABC120", "DEF450", "123450"],  # 十六进制，6位，末尾补0
        "17": ["ABC340", "DEF670", "123560"],  # 十六进制，6位，末尾补0
        "10": ["4545454545", "6767676767", "3232323232"]  # 未指定格式，默认10位
    }

    return fixed_card_numbers


def generate_dict_data():
    # 定义access_mode字典数据，只保留第2列(dict_code)和第4列(dict_note)
    access_mode_data = [
        (1, "UDP-盈佳"),
        (2, "UDP-力维"),
        (7, "HTTP-大华"),
        (3, "UDP-亚奥"),
        (4, "UDP-海能"),
        (5, "UDP-邦讯-新版"),
        (6, "UDP-高新兴"),
        (8, "SDK-大华"),
        (13, "UDP-中达"),
        (12, "TCP-力维"),
        (14, "UDP-CH803LM"),
        (15, "UDP-ES1000"),
        (16, "UDP-邦讯-旧版"),
        (17, "TCP-邦讯-旧版"),
        (10, "UDP-高新兴V2"),
        (9, "SDK-海康威视")
    ]

    # 获取固定卡号枚举值，用于过滤未匹配的类型
    fixed_card_numbers = generate_card_numbers()

    # 生成结果列表
    result = []

    # 遍历数据，只生成有对应卡号配置的用户
    for dict_code, dict_note in access_mode_data:
        # 检查该类型是否有对应的卡号配置
        if str(dict_code) in fixed_card_numbers:
            # 版本1：已授权
            name_1 = f"{dict_note}1_已授权"
            # 版本2：未授权
            name_2 = f"{dict_note}_未授权"

            # 添加到结果列表
            result.append((name_1, dict_code, dict_note))
            result.append((name_2, dict_code, dict_note))
        else:
            print(f"警告: 类型 {dict_code} ({dict_note}) 没有对应的卡号配置，跳过生成用户")

    return result


def generate_delete_inserts():
    # 获取生成的用户数据,清空已有用户,初始化
    user_data = generate_dict_data()

    # 生成SQL删除语句
    sql_list = []

    # 生成查询语句，检查用户是否存在
    check_sql = "SELECT name FROM entrance_user WHERE name IN ("
    names = [name for name, dict_code, dict_note in user_data]
    check_sql += ",".join([f"'{name}'" for name in names])
    check_sql += ");"

    # 添加查询语句到结果列表
    sql_list.append(f"-- 检查生成的用户是否存在")
    sql_list.append(check_sql)
    sql_list.append("")

    # 生成删除语句
    sql_list.append(f"-- 删除已存在的生成用户")
    for name, dict_code, dict_note in user_data:
        delete_sql = f"DELETE FROM `entrance_user` WHERE `name` = '{name}' OR `code` = '{name}';"
        sql_list.append(delete_sql)

    return sql_list


def generate_sql_inserts():
    # 获取生成的用户数据
    user_data = generate_dict_data()

    # 固定值
    user_type = 2
    dept_id = "f677d76e-8345-4b16-b70d-a9043079808a"
    no = ""
    relation_person = "fd08df32-495c-4bc1-9359-ee6c8b18caaa"

    # 生成SQL插入语句
    sql_list = []

    for name, dict_code, dict_note in user_data:
        # 生成UUID
        import uuid
        user_uuid = get_need_uuid4()

        # 生成当前时间
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构建SQL语句
        sql = f"""INSERT INTO `entrance_user` (`uuid`, `name`, `user_type`, `dept_id`, `no`, `code`, `relation_person`, `mobile`, `phone`, `sex`, `fax`, `mail`, `post`, `address`, `descr`, `picture`, `is_sys_sync`, `isdel`, `create_time`, `update_time`) VALUES ('{user_uuid}', '{name}', {user_type}, '{dept_id}', '{no}', '{name}', '{relation_person}', '16425523422', '', 1, '', '', '', '', NULL, NULL, 0, 0, '{current_time}', '{current_time}');"""

        sql_list.append(sql)

    return sql_list


def add_power(fixed_card_numbers, user_names=None):
    """
    为用户添加门禁权限
    :param fixed_card_numbers: 固定卡号枚举值
    :param user_names: 用户名称列表，为空则直接返回，不处理任何用户
    """
    relation_person = "fd08df32-495c-4bc1-9359-ee6c8b18caaa"

    # 如果user_names为空，直接返回，不处理任何用户
    if not user_names:
        print("未提供用户名称列表，跳过权限添加")
        return

    # 去重，避免重复处理同一用户
    unique_user_names = list(set(user_names))

    # 批量查询用户信息
    user_names_str = ",".join([f"'{name}'" for name in unique_user_names])
    user_ids_sql = f"select uuid, name from entrance_user where name in ({user_names_str});"
    users = conn_obj.select(sql=user_ids_sql)

    if not users:
        print("未查询到任何用户，跳过权限添加")
        return

    # 获取用户数据，用于匹配用户类型
    user_data = generate_dict_data()
    unique_access_modes = {}
    for name, code, note in user_data:
        unique_access_modes[note] = code

    # 查询设备信息
    precinct_id = '01-01-17-02-05-01'
    device_query = f"select device_id, access_mode from access_control_device where room_id = '{precinct_id}' and door_name != '';"
    device_list = conn_obj.select(sql=device_query)

    # 按设备类型分组，确保设备ID唯一
    devices_by_type = {}
    for device_id, access_mode in device_list:
        if access_mode:
            access_mode_str = str(access_mode)
            if access_mode_str not in devices_by_type:
                devices_by_type[access_mode_str] = set()  # 使用集合确保设备ID唯一
            devices_by_type[access_mode_str].add(device_id)

    # 将集合转换为列表
    for mode in devices_by_type:
        devices_by_type[mode] = list(devices_by_type[mode])

    # 遍历每个用户，简化循环结构
    for user_id, user_name in users:
        print(f"正在处理用户: {user_name} (ID: {user_id})")

        # 匹配用户类型
        user_type = None
        for note, code in unique_access_modes.items():
            if user_name.startswith(note):
                user_type = code
                break

        if not user_type:
            print(f"警告: 未找到用户 {user_name} 对应的类型信息，跳过处理")
            continue

        user_type_str = str(user_type)

        # 检查类型是否有对应的卡号和设备
        if user_type_str not in fixed_card_numbers or user_type_str not in devices_by_type:
            print(f"警告: 类型 {user_type} 没有对应的卡号或设备配置，跳过处理")
            continue

        # 获取设备列表和卡号列表
        device_list = devices_by_type[user_type_str]
        card_list = fixed_card_numbers[user_type_str]

        # 根据授权状态选择卡号
        if "已授权" in user_name:
            # 已授权用户：使用前2个卡号
            user_card_list = card_list[:2]
        else:
            # 未授权用户：使用最后一个卡号
            user_card_list = [card_list[-1]]

        # 清除用户的旧卡片和权限
        for card in user_card_list:
            print(f"  准备为用户 {user_name} 添加卡片: {card}")
            conn_obj.insertone(sql=f"delete from entrance_card where card_id = '{card}';")
            conn_obj.insertone(sql=f"delete from entrance_card_auth where card_id = '{card}';")

        # 为用户添加新卡片和权限
        for card in user_card_list:
            # 查询最新的max(id)
            max_id_sql = "select max(id) from entrance_card"
            max_id_result = conn_obj.select(sql=max_id_sql)
            current_max_id = max_id_result[0][0] if max_id_result[0][0] else 0
            new_card_id = current_max_id + 1

            # 添加卡片
            add_card_sql = f"""
                insert into entrance_card (`id`, `card_id`, `belong_user`, `current_user`, `create_user`, `create_time`, `isdel`)
                values ('{new_card_id}', '{card}', '{user_id}', '{user_id}', '{user_id}', now(), 0);
            """
            conn_obj.insertone(sql=add_card_sql)

            # 为该卡片添加权限
            for device_id_val in device_list:
                print(f"正在处理设备: {device_id_val}")
                # 先删除该卡片在该设备上的权限
                conn_obj.insertone(
                    sql=f"delete from entrance_card_auth where card_id = '{card}' and device_id = '{device_id_val}'");

                # 添加新权限
                add_auth_sql = f"""
                    insert into entrance_card_auth(`card_id`, `device_id`, `user_id`, `password`, `expiration`, `isdel`, `current_user`, `create_user`, `create_time`, `update_time`)
                    VALUES('{card}', '{device_id_val}', null,
                    NULL , '2026-01-17', 0, '{user_id}', '{relation_person}', now(), now());
                """
                conn_obj.insertone(sql=add_auth_sql)

        print(
            f"  用户 {user_name} 授权完成，添加了 {len(user_card_list)} 个卡片，每个卡片授权给 {len(device_list)} 个设备")
        print("-" * 50)


if __name__ == "__main__":
    # 生成完整的SQL脚本：检查->删除->插入
    full_sql = []

    # 1. 添加注释和标题
    full_sql.append("-- 广东门禁-撤权数据准备：批量生成用户")
    full_sql.append(f"-- 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    full_sql.append("")

    # 2. 生成检查和删除语句
    delete_sql = generate_delete_inserts()
    full_sql.extend(delete_sql)
    full_sql.append("")

    # 3. 生成插入语句
    insert_sql = generate_sql_inserts()
    full_sql.append("-- 插入新生成的用户")
    full_sql.extend(insert_sql)

    # 4. 打印结果
    for line in full_sql:
        print(line)

    # 5. 将结果保存到文件
    output_file = os.path.join(os.path.dirname(__file__), "entrance_user_full.sql")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in full_sql:
            f.write(f"{line}\n")

    print(f"\n完整SQL脚本已生成并保存到: {output_file}")
    print(f"共生成 {len(delete_sql) - 3} 条删除语句和 {len(insert_sql)} 条插入语句")
    print(f"脚本包含：检查用户存在性 -> 删除已存在用户 -> 插入新用户")

    # 6. 执行生成的SQL脚本
    print("\n" + "=" * 60)
    print("开始执行生成的SQL脚本...")
    print("=" * 60)

    # 初始化数据库连接
    conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])

    # 读取并执行SQL文件
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 按分号分割SQL语句
        sql_statements = sql_content.split(';')
        print(f"按分号分割后共得到 {len(sql_statements)} 条语句")

        executed_count = 0
        skipped_count = 0

        for i, sql_block in enumerate(sql_statements):
            # 去除两端空格
            sql_block = sql_block.strip()
            if not sql_block:
                print(f"\n处理第 {i + 1} 条语句块:")
                print(f"  跳过: 空语句块")
                skipped_count += 1
                continue

            # 逐行处理语句块，过滤掉注释行
            lines = sql_block.split('\n')
            actual_sql_lines = []
            for line in lines:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('--'):
                    continue
                actual_sql_lines.append(line)

            # 将剩余行拼接成实际的SQL语句
            actual_sql = ' '.join(actual_sql_lines)
            actual_sql = actual_sql.strip()

            if not actual_sql:
                print(f"\n处理第 {i + 1} 条语句块:")
                print(f"  跳过: 仅包含注释和空行")
                skipped_count += 1
                continue

            print(f"\n处理第 {i + 1} 条语句块:")
            print(f"  实际SQL: {repr(actual_sql[:100])}..." if len(
                actual_sql) > 100 else f"  实际SQL: {repr(actual_sql)}")

            try:
                if actual_sql.upper().startswith('SELECT'):
                    # 对于SELECT语句，使用查询方法
                    print(f"  执行: SELECT语句")
                    conn_obj.select(sql=actual_sql)
                elif actual_sql.upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                    # 对于INSERT、UPDATE、DELETE语句，使用insertone方法
                    print(f"  执行: {actual_sql[:6].upper()}语句")
                    conn_obj.insertone(sql=actual_sql)
                else:
                    # 对于其他类型的语句，尝试使用通用方法（如果有）
                    print(f"  执行: 其他类型语句")
                    if hasattr(conn_obj, 'execute'):
                        conn_obj.execute(sql=actual_sql)
                    else:
                        # 如果没有通用方法，尝试使用insertone
                        conn_obj.insertone(sql=actual_sql)

                executed_count += 1
                print(f"  结果: 执行成功")
            except Exception as e:
                print(f"  结果: 执行失败")
                print(f"  错误信息: {e}")

        print(
            f"\nSQL脚本执行完成，共分割出 {len(sql_statements)} 条语句块，跳过 {skipped_count} 个块，执行 {executed_count} 条SQL语句")
    except Exception as e:
        print(f"执行SQL脚本时出错: {e}")

    # 7. 批量为生成的用户添加门禁权限
    print("\n" + "=" * 60)
    print("开始为生成的用户添加门禁权限...")
    print("=" * 60)

    # 获取生成的用户名称列表
    user_data = generate_dict_data()
    user_names = [name for name, dict_code, dict_note in user_data]

    # 生成固定卡号枚举值
    card_numbers = generate_card_numbers()

    # 调用add_power函数，为所有生成的用户添加权限
    add_power(card_numbers, user_names)

    print("\n" + "=" * 60)
    print("所有用户权限添加完成！")
    print("=" * 60)
