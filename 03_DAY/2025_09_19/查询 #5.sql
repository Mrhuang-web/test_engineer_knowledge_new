SELECT 
    c.TABLE_SCHEMA AS '数据库',
    c.TABLE_NAME AS '表名',
    t.TABLE_COMMENT AS '表注释',
    c.COLUMN_NAME AS '字段名',
    c.COLUMN_COMMENT AS '字段注释' 
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN INFORMATION_SCHEMA.TABLES t
    ON c.TABLE_SCHEMA = t.TABLE_SCHEMA
    AND c.TABLE_NAME = t.TABLE_NAME
WHERE c.COLUMN_NAME LIKE '%clogusrname%'
  AND c.TABLE_SCHEMA = 'spider2';
  




SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%上海定制6%"

INSERT INTO `t_cfg_precinct` (`precinct_id`, `lsc_id`, `precinct_name`, `up_precinct_id`, `precinct_kind`, `isdel`, `update_time`, `access_time`, `area_code`, `access_type`, `description`, `building_type`, `room_kind`, `air_type`, `refrigeration_mode`, `resource_code`, `leader`, `leader_name`, `leader_phone`, `address`, `resource_origin`, `resource_name`, `scene`, `imp_remark`, `room_business_type`, `room_status`) 
VALUES ('01-01-08-04-13-03-01', '1', '黄某某_上海定制6_机楼3_机房1', '01-01-08-04-13-03', 5, 000, '2025-09-19 18:46:36', NULL, NULL, 0, NULL, 1, 001, 2, '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO `t_cfg_precinct` (`precinct_id`, `lsc_id`, `precinct_name`, `up_precinct_id`, `precinct_kind`, `isdel`, `update_time`, `access_time`, `area_code`, `access_type`, `description`, `building_type`, `room_kind`, `air_type`, `refrigeration_mode`, `resource_code`, `leader`, `leader_name`, `leader_phone`, `address`, `resource_origin`, `resource_name`, `scene`, `imp_remark`, `room_business_type`, `room_status`) 
VALUES ('01-01-08-04-13-03-02', '1', '黄某某_上海定制6_机楼3_机房2', '01-01-08-04-13-03', 5, 000, '2025-09-19 18:46:36', NULL, NULL, 0, NULL, 1, 001, 2, '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);



#########################################    FSU - 接入    #######################################






# 第一步
# 	00001006000000154108   414213413123
SELECT    * FROM   t_cfg_device LIMIT 10;
SELECT    * FROM   t_cfg_device    WHERE device_id="00001006000000030266"  AND   device_code="80000001233";
SELECT    * FROM   t_cfg_device    WHERE device_id="00001006000000154070"  AND   device_code="2631264872312";
SELECT    * FROM   t_cfg_device    WHERE device_id="00001006000000154108"  AND   device_code="414213413123";
SELECT    * FROM   t_cfg_device    WHERE device_id="00001006000000154147"  AND   device_code="847272716181";

SELECT    * FROM   t_cfg_device    WHERE device_name LIKE "%黄某某%";
SELECT    * FROM   t_cfg_device    WHERE device_name LIKE "%徐%";
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-23-03-06-01-02';




# 第二步   如果已有，不需要新增
INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, 
`sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, 
`purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, 
`version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, 
`load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, 
`actual_start_time`, `join`) VALUES ('100012340101', '00001006000000153697', '上海定制-fsu', 
'01-01-07-03-05-02', 1, NULL, 000, NULL, 13, NULL, 76, 3, NULL, '265224658376469', 
1617, 1, NULL, NULL, NULL, '2023-01-04 19:54:25', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 
7012673, NULL, NULL, NULL, NULL, NULL, 0, 0, 102, NULL, NULL, NULL, NULL);



# 第三步
# 	00001006000000154070   2631264872312
SELECT * FROM t_cfg_fsu  LIMIT 100;
SELECT * FROM t_cfg_fsu  WHERE  device_id="00001006000000154661"; 
SELECT * FROM t_cfg_fsu  WHERE  device_id="00001006000000154662"; 

SELECT * FROM t_cfg_fsu  WHERE  device_id="00001006000000154737"; 
SELECT * FROM t_cfg_fsu  WHERE  device_id="00001006000000154738"; 

SELECT * FROM t_cfg_fsu  where address='10.12.12.186' AND  device_id="00001006000000154070" ;
SELECT * FROM t_cfg_fsu  where address='10.12.12.186' AND  device_id="00001006000000154108" ;
SELECT * FROM t_cfg_fsu  where address='10.12.12.186' AND  device_id="00001006000000154147" ;

# 第四步
SELECT * FROM t_cfg_nmsdevice LIMIT 10;
# 	00001006000000154070   2631264872312
SELECT * FROM t_cfg_nmsdevice where device_id = '00001006000000030266' LIMIT 10;
SELECT * FROM t_cfg_nmsdevice where device_id = '00001006000000154070' LIMIT 10;
SELECT * FROM t_cfg_nmsdevice where device_id = '00001006000000154108' LIMIT 10;
SELECT * FROM t_cfg_nmsdevice where device_id = '00001006000000154147' LIMIT 10;


# 第五步
INSERT INTO t_cfg_nmsdevice
(device_id, service_addr, service_port, up_server_id, web_page, login_state, sip_port, private_service_addr, subnetmask, gateway, rtsp_port, http_port, icpu_summit, imem_summit, isend_summit, irecv_summit, nms_type)
VALUES('00001006000000154738', '127.0.0.1', 3306, NULL, NULL, NULL, NULL, '10.1.5.109', NULL, NULL, NULL, 8086, NULL, NULL, NULL, NULL, 101);



# 第六步
SELECT b.service_addr,b.service_port,b.private_service_addr,b.rtsp_port,a.* FROM t_cfg_device a INNER JOIN t_cfg_nmsdevice b ON a.device_id=b.device_id limit 100;




# 第七步  -- 中间库中看   22244431123123 \ 442123123131412
SELECT * FROM fsu  where fsuid =  '847272716181' LIMIT 100;



# 第八步  -- 查数据、删数据    
SELECT * FROM fsu LIMIT 10;
SELECT * FROM device LIMIT 10;
SELECT * FROM signals LIMIT 10;
SELECT * FROM storage LIMIT 10;
SELECT * FROM threshold LIMIT 10;
SELECT * FROM t_cfg_mete LIMIT 10;


# 2241234412313   22244431123123 \ 442123123131412
SELECT * FROM fsu WHERE fsuname LIKE "%黄某某%";
SELECT * FROM fsu WHERE fsuid = '414213413123';




# 第九步  -- 中间库条件筛选
SELECT * FROM t_cfg_precinct  LIMIT 10;
SELECT * FROM t_cfg_precinct  WHERE precinct_name LIKE "%黄某某%";

#80000001233
SELECT * FROM t_cfg_mete WHERE mete_name LIKE '%温度%' LIMIT 100;
SELECT * FROM signals LIMIT 100;

SELECT * FROM fsu WHERE fsuid = '414213413123';
SELECT * FROM device WHERE fsuid = '414213413123';
SELECT * FROM signals WHERE fsuid = '414213413123';
SELECT * FROM t_cfg_mete WHERE mete_code = '012329';

SELECT * FROM fsu WHERE fsuid = '80000001233';
SELECT * FROM device WHERE fsuid = '80000001233';
SELECT * FROM signals WHERE fsuid = '80000001233';
SELECT * FROM t_cfg_mete WHERE mete_code = '012329';


SELECT * FROM fsu WHERE fsuid = '847272716181';
SELECT * FROM device WHERE fsuid = '847272716181';
SELECT * FROM signals WHERE fsuid = '847272716181' AND signalsid='012329';
SELECT * FROM t_cfg_mete WHERE mete_code = '012329';


INSERT INTO `t_cfg_mete` (`mete_code`, `device_type`, `mete_name`, `mete_kind`, `raw_mete_kind`, `unit`, `mete_explain_type`, `alarm_note`, `alarm_explain`, `remark`, `link_mete_code`, `up_mete_code`, `logical_type`, `sub_logical_type`, `vipmete_flag`, `up_effect`, `low_effect`, `flag2g`) 
VALUES ('012329', '12', '二次侧回液温度', 1, 3, '℃', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL);




# 'manufacturer_id',
SELECT * FROM t_cfg_dict WHERE col_name IN ('device_type','access_type','province_index');
SELECT * FROM t_cfg_device WHERE device_type = 76 and access_type = 1;


# 第十步  -- 动环库查看设备测点
SELECT * FROM t_cfg_fsu LIMIT 10;
SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail LIMIT 10;
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154147';
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000154159';
SELECT * FROM t_cfg_mete WHERE mete_code = '012329';
SELECT * FROM t_cfg_metemodel_detail  WHERE mete_code = '012329';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000016751' AND mete_kind != '4'

SELECT * FROM t_cfg_metemodel_detail WHERE mete_code = '012329'











