[上海]批量机房_机柜 [目前手工到14，还有80多个未组测上报] 
    需要在TestEnv,加上sh数据库的连接方式
    需要扩张点：把单机楼-单机房，变成单机楼-多机房形式
    都需要控制延时：6s,否则太频繁接口会错误
    且每次修改文件后，需要文本打开，另存为，改成utf8格式
    逐步运行脚本
    
    第一步：使用make_floor()函数创建楼栋            - doc的flood_name.csv
        不涉及sql
    
    第二步：使用make_room()函数创建机房             - doc的room_name.csv
        涉及sql
            SELECT * FROM t_cfg_precinct where precinct_name LIKE "上海楼栋%" ORDER BY precinct_id;
            复制处precinct_id列到room_name.csv的precinct_id列
            
    
    第三步：使用make_cabinet_columns()函数创建机柜  - doc的cabinet_columns_name.csv
        涉及sql[目前把查询的，手工复制到excel] -- 需要手工排序precinct_id列
            SELECT * FROM (SELECT c.precinct_name AS '站点' ,b.precinct_name AS '楼栋',a.precinct_name AS '机房',a.precinct_id FROM t_cfg_precinct a INNER JOIN t_cfg_precinct b ON a.up_precinct_id = b.precinct_id
            INNER JOIN  t_cfg_precinct c ON b.up_precinct_id = c.precinct_id
            WHERE a.precinct_name LIKE "上海机房%") e  order BY e.precinct_id DESC ;
        
            
    第四步：使用make_cabinet()函数创建设备          - doc的cabinet_name.csv
        涉及sql[目前手工复制到excel] -- 需要手工排序cabinet_columns_number 列
            SELECT precinct_tree.站点,precinct_tree.楼栋,precinct_tree.机房,ec.cabinet_column_number,ec.cabinet_column_name,ec.id
            FROM energy_cabinet_column ec
            JOIN (
                SELECT 
                    c.precinct_name AS `站点`,
                    b.precinct_name AS `楼栋`,
                    a.precinct_name AS `机房`,
                    a.precinct_id
                FROM t_cfg_precinct a
                JOIN t_cfg_precinct b ON a.up_precinct_id = b.precinct_id
                JOIN t_cfg_precinct c ON b.up_precinct_id = c.precinct_id
                WHERE a.precinct_name LIKE '上海机房%'
            ) AS precinct_tree ON precinct_tree.precinct_id = ec.precinct_id;
    
    第五步：写入设备到动环
        涉及创建的机房前缀
        涉及sql语句
        SELECT device_code,device_name FROM  t_cfg_device WHERE device_code LIKE  '%20250922%'

    第五步：使用sim_fsu项目,实现设备接入                 - B接口.csv
        涉及到新脚本 - 数据准备批量.py
        还需要涉及到性能脚本jmeter中的上报和上报配置 【未实现】
            避免上报太频繁
    
    第六步：使用sim_code,实现测点写入
        脚本还未实现
        涉及sql语句 -- 需要手工排序precinct_id 列
            SELECT
                mm.device_type,
                mm.mete_id,
                mm.mete_code,
                mm.up_mete_id,
                mm.mete_kind,
                mm.mete_no,
                d.device_id,
                d.device_name,
                d.device_model,
                pt.precinct_name,
                pt.station_name,
                pt.floor_name,
                pt.cab_name,
                pt.col_name
            FROM t_cfg_metemodel_detail mm
            JOIN (
                SELECT '分路XX相电流Ia' AS up_mete_id UNION ALL
                SELECT '分路XX相电流Ib' UNION ALL
                SELECT '分路XX相电流Ic' UNION ALL
                SELECT '分路XX相电压Ua' UNION ALL
                SELECT '分路XX相电压Ub' UNION ALL
                SELECT '分路XX相电压Uc' UNION ALL
                SELECT '分路XX有功功率Pa' UNION ALL
                SELECT '分路XX有功功率Pb' UNION ALL
                SELECT '分路XX有功功率Pc'
            ) mf ON mm.up_mete_id = mf.up_mete_id
            JOIN t_cfg_device d ON d.device_model = mm.model_id
            JOIN (
                SELECT
                    p5.precinct_id AS col_id,
                    p5.precinct_name AS col_name,
                    p4.precinct_name AS cab_name,
                    p3.precinct_name AS floor_name,
                    p2.precinct_name AS station_name,
                    p1.precinct_name AS precinct_name
                FROM t_cfg_precinct p1
                JOIN t_cfg_precinct p2 ON p2.up_precinct_id = p1.precinct_id
                JOIN t_cfg_precinct p3 ON p3.up_precinct_id = p2.precinct_id
                JOIN t_cfg_precinct p4 ON p4.up_precinct_id = p3.precinct_id
                JOIN t_cfg_precinct p5 ON p5.up_precinct_id = p4.precinct_id
            ) pt ON d.precinct_id = pt.col_id
            WHERE d.precinct_id LIKE '01-01-08-04-15-%'
              AND d.device_name = 'UPS配电';






[集团]液冷_数据准备 [描述 - 都是基于C接口中间库做操作] 
    原始：
        get_sql_result 
        create_activealarm           -- 造告警时用
        create_activealarm_by_time   -- 造告警时用
        create_tah                   -- 造数据时用
        
    更改：
        create_activealarm           -- 造告警时用
        create_tah_by_device_signal  -- 造数据时用
        get_sql_result

    函数明细：
        执行说明：
            先调用create_activealarm或create_activealarm_by_time生成告警  -- 会生成sql文件,需要检查下 -- 手动去执行插入
            最后是create_tah -- 生成告警的数据 --手动去执行插入
        get_sql_result
            连接数据库：函数接收sql,连接后查询,返回查询后的sql结果 - 列表形式
        create_activealarm - 实时告警
            参数：
                生成的数量
                生成的文件
                站点id -- 中间库-即数据准备中设置的站点id
            查询中间库：
                信号表[主要是站点-机房-设备-是否以及写入对应测点)  - 写入了才能进行造数，否则匹配不到]
                告警信息表[主要是告警信息 - 拿最新的一条的id+1,作为本次插入的id]
                写入告警信息表[主要是对指定站点进行告警的生成]
        create_activealarm_by_time - 历史告警
            参数：
                生成的数量
                生成的文件
                站点id -- 中间库-即数据准备中设置的站点id
                开始时间 - 格式：YYYY-MM-DD HH:MM:SS
                结束时间 - 格式：YYYY-MM-DD HH:MM:SS
            查询中间库：
                信号表[主要是站点-机房-设备-是否以及写入对应测点)  - 写入了才能进行造数，否则匹配不到]
                告警信息表[主要是告警信息 - 拿最新的一条的id+1,作为本次插入的id]
                写入告警信息表[主要是对指定站点进行告警的生成，时间在指定范围内]
        create_tah - 全量历史数据[这里补充]
            查询中间库：
                信号表[主要是站点-机房-设备-是否以及写入对应测点)  - 写入了才能进行造数，否则匹配不到]
            