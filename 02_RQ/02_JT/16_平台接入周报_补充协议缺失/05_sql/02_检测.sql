select
    distinct
    provice as '省',
        city as '市',
        siteName as '站点',
        building as '楼栋名称',
        roomName as '机房名称',
        deviceName as '设备名称',
        deviceTypeName as '设备类型',
        sub_device_type as '设备子类' ,
        rated_power as '额定容量',
        unit as '单位',
        devicesys_name as '系统名称',
        sysType as '系统类型',
        work_style as '备份方式',
        current_ele as '充电电流' ,
        use_end_time as '报废时间',
        device_principal as '负责人',
        leader_phone as '电话'
from
    (
        select
            t1.precinct_name AS provice,
            t2.precinct_name AS city,
            st.precinct_name AS siteName,
            bd.precinct_name AS building,
            rm.precinct_name AS roomName,
            d.device_name AS deviceName,
            d.device_type,
            dict.dict_note AS deviceTypeName,
            d.sub_device_type AS sub_device_type,
            d.device_id,
            d.rated_power+0 AS rated_power,
            d.unit AS unit,
            ifnull(sys.devicesys_name,gsys.devicesys_name) AS devicesys_name,
            ifnull(sys.pe_entity_type,gsys.pe_entity_type) AS sysType,
            sys.work_style,
            ifnull(sys.current_ele,gsys.current_ele) AS current_ele,
            DATE_FORMAT(d.use_end_time, '%Y-%m-%d') AS use_end_time,
            d.device_principal,
            d.leader_phone

        from t_cfg_device d
                 left join t_cfg_precinct rm on rm.precinct_id = d.precinct_id
                 left join t_cfg_precinct bd on bd.precinct_id = rm.up_precinct_id and bd.precinct_kind = 3
                 left join t_cfg_precinct st on st.precinct_id = ifnull(bd.up_precinct_id,rm.up_precinct_id) and st.precinct_kind = 2
                 left join t_cfg_site sitetype on sitetype.site_id = st.precinct_id
                 LEFT JOIN t_cfg_devicesys_detail de ON de.sub_id = d.device_id #关系统
	LEFT JOIN t_cfg_devicesys sys ON de.devicesys_id = sys.devicesys_id
            left join t_cfg_gyzlsys_detail gde1 on gde1.sub_id = d.device_id and gde1.item_type = 2
            left join t_cfg_gyzlsys_detail gde2 on gde2.sub_id = gde1.devicesys_id
            left join t_cfg_gyzlsys gsys on gsys.devicesys_id = gde2.devicesys_id
            LEFT JOIN t_cfg_precinct t1 ON t1.precinct_id = LEFT (d.precinct_id, 5 )
            LEFT JOIN t_cfg_precinct t2 ON t2.precinct_id = LEFT (d.precinct_id, 8 )
            LEFT JOIN t_cfg_dict dict ON dict.col_name = 'device_type'  AND d.device_type = dict.dict_code
        WHERE
            d.device_type IN(6,7,8)
          and sitetype.site_type in(1,2)
          AND d.resource_code > 1
          AND d.lsc_id > 1
          AND d.isdel = 0
          AND t1.precinct_id LIKE "01-1%2"
    ) as table1
where  table1.devicesys_name is null  or  table1.rated_power is null
   or (table1.device_type=6 and (table1.sub_device_type not in(11,12,13,14,15) or table1.sub_device_type is null) )
   or (table1.device_type=8 and (table1.sub_device_type not in(1,2,3,4,5) or table1.sub_device_type is null))
ORDER BY  convert(table1.provice using gbk),convert(table1.city using gbk),convert(table1.siteName using gbk),convert(table1.roomName using gbk) ,convert(table1.deviceName using gbk)  asc;






SELECT * FROM t_cfg_precinct WHERE char_length(precinct_id) = 5;


SELECT * FROM t_cfg_precinct WHERE precinct_name = '安徽蚌埠市蚌山区0476数据中心'
