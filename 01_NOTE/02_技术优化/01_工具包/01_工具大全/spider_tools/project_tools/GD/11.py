import os

print("开始执行生成的SQL脚本...")
print("=" * 60)

# 初始化数据库连接

output_file = os.path.join(os.path.dirname(__file__), "entrance_user_full.sql")

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
        print(f"  实际SQL: {repr(actual_sql[:100])}..." if len(actual_sql) > 100 else f"  实际SQL: {repr(actual_sql)}")

        try:
            if actual_sql.upper().startswith('SELECT'):
                # 对于SELECT语句，使用查询方法
                print(f"  执行: SELECT语句")
                print(actual_sql)
            elif actual_sql.upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                # 对于INSERT、UPDATE、DELETE语句，使用insertone方法
                print(f"  执行: {actual_sql[:6].upper()}语句")
                print(actual_sql)
            else:
                # 对于其他类型的语句，尝试使用通用方法（如果有）
                print(f"  执行: 其他类型语句")
                print(actual_sql)

            executed_count += 1
            print(f"  结果: 执行成功")
        except Exception as e:
            print(f"  结果: 执行失败")
            print(f"  错误信息: {e}")

    print(
        f"\nSQL脚本执行完成，共分割出 {len(sql_statements)} 条语句块，跳过 {skipped_count} 个块，执行 {executed_count} 条SQL语句")
except Exception as e:
    print(f"执行SQL脚本时出错: {e}")

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
        print(f"  实际SQL: {repr(actual_sql[:100])}..." if len(actual_sql) > 100 else f"  实际SQL: {repr(actual_sql)}")

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