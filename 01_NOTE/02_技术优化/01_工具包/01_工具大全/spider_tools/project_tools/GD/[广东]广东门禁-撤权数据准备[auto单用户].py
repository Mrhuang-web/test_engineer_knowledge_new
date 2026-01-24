# [广东]广东门禁-撤权数据准备.py
import os
import time

# 仅在需要使用原有功能时导入相关模块

import requests
import spider_tools.Common.TestEnv as TestEnv
from asptest.common.mysqlpool import MySQLHelper

conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])


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
    # 定义用户名
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

    # 生成结果列表
    result = []

    # 遍历数据，生成两种版本的用户名称
    for dict_code, dict_note in access_mode_data:
        # 版本1：已授权
        name_1 = f"{dict_note}1_已授权"
        # 版本2：未授权
        name_2 = f"{dict_note}_未授权"

        # 添加到结果列表
        result.append((name_1, dict_code, dict_note))
        result.append((name_2, dict_code, dict_note))

    return result


def generate_delete_inserts():
    # 获取生成的用户数据
    user_data = generate_dict_data()

    # 生成SQL删除语句
    sql_list = []

    # 生成查询语句，检查用户是否存在
    check_sql = "SELECT name FROM entrance_user WHERE name IN ("
    names = [name for name, dict_code, dict_note in user_data]
    check_sql += ",".join([f"'{name}'" for name in names])
    check_sql += ")"

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
        user_uuid = str(uuid.uuid4())

        # 生成当前时间
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构建SQL语句
        sql = f"""INSERT INTO `entrance_user` (`uuid`, `name`, `user_type`, `dept_id`, `no`, `code`, `relation_person`, `mobile`, `phone`, `sex`, `fax`, `mail`, `post`, `address`, `descr`, `picture`, `is_sys_sync`, `isdel`, `create_time`, `update_time`) VALUES ('{user_uuid}', '{name}', {user_type}, '{dept_id}', '{no}', '{name}', '{relation_person}', '16425523422', '', 1, '', '', '', '', NULL, NULL, 0, 0, '{current_time}', '{current_time}');"""

        sql_list.append(sql)

    return sql_list


def add_power(fixed_card_numbers):
    user_ids = """ select uuid from entrance_user where name = 'auto用户' """
    user_id = conn_obj.select(sql=user_ids)[0][0]
    user_cart = f""" select card_id from entrance_card where belong_user = '{user_id}' """
    user_cart = conn_obj.select(sql=user_cart)

    precinct_id = '01-01-17-02-05-01'
    device_id = f""" select device_id,access_mode from access_control_device where room_id = '{precinct_id}' and door_name != '' """
    device_ids = conn_obj.select(sql=device_id)
    uniques = set()

    # 删除已有的卡号
    for cart_id in user_cart:
        for device, numbers in fixed_card_numbers.items():
            if str(cart_id[0]) in numbers:
                delete_card = f"""
                    delete from entrance_card where card_id = '{cart_id[0]}'
                    """
                conn_obj.insertone(sql=delete_card)

    return None

    # 遍历固定卡号枚举值，将不在用户卡片中的卡号添加到集合中
    for device, numbers in fixed_card_numbers.items():
        for cart_id in numbers[0:2]:
            uniques.add(cart_id)

    # 遍历集合，添加卡数据
    if uniques:
        for card_id in uniques:
            max_id = conn_obj.select(sql="select max(id) from entrance_card")[0][0]
            max_id += 1
            add_power_sql = f"""
            insert into entrance_card (`id`,`card_id`, `belong_user`, `current_user`,`create_user`,`create_time`,`isdel`)
            values ('{max_id}', '{card_id}', '{user_id}', '{user_id}', '{user_id}', now(), 0)
            """
            conn_obj.insertone(sql=add_power_sql)

    # 遍历设备ID列表，删除卡权限
    for device_id, access_mode in device_ids:
        if access_mode:
            card = fixed_card_numbers[str(access_mode)]
            for card_id in card:
                delete_sql = f"""
                    delete from entrance_card_auth where card_id = '{card_id}' and device_id = '{device_id}'
                    """
                conn_obj.insertone(sql=delete_sql)



    for device_id, access_mode in device_ids:
        if access_mode:
            card = fixed_card_numbers[str(access_mode)][0:1]
            for card_id in card:
                insert_sql = f"""
                    insert into entrance_card_auth(`card_id`, `device_id`, `user_id`, `password`, `expiration`, `isdel`, `current_user`, `create_user`, `create_time`, `update_time`)
                    VALUES('{card_id}', '{device_id}', null,
                    NULL , '2026-01-17', 0, '{user_id}', '{user_id}', now(), now())
                    """
                conn_obj.insertone(sql=insert_sql)


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

    # 原有的门禁权限处理功能
    card_numbers = generate_card_numbers()
    add_power(card_numbers)
