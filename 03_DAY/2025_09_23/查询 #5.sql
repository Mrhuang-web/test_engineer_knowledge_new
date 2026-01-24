
SELECT e.precinct_name,TCT.* FROM t_cfg_precinct e JOIN 
(SELECT                 
            mm.device_type,
            mm.mete_id,
            mm.mete_code,
              mm.up_mete_id,
              mm.mete_kind,
              t.device_id,
              t.device_name,
              t.precinct_name,    -- 院区名称  差站点、楼栋
              mm.up_mete_id,
            t.device_id,        -- 以下按需保留设备字段
            mm.mete_no,
            mm.up_mete_id,
            t.precinct_id		-- 还要关联机柜和机柜列
            FROM    t_cfg_metemodel_detail mm
            JOIN   (
                    SELECT  p.precinct_name,
									 p.up_precinct_id,
                            d.*          -- 这里已含 device_model，别再加一次
                    FROM    t_cfg_precinct p
                    JOIN    t_cfg_device d
                           ON d.precinct_id = p.precinct_id
                    WHERE   d.precinct_id LIKE '01-01-08-04-15-%'
                      AND   d.device_name = 'UPS配电'
                   ) AS t
             ON mm.model_id = t.device_model AND up_mete_id IN 
             ("分路XX相电流Ia","分路XX相电流Ib","分路XX相电流Ic","分路XX相电压Ua","分路XX相电压Ub","分路XX相电压Uc","分路XX有功功率Pa","分路XX有功功率Pb","分路XX有功功率Pc")
) AS TCT ON  e.precinct_id = TCT.up_precinct_id 
				;
				
				
				
				
				
				
				
				
				
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
  


SELECT * FROM t_cfg_mete LIMIT 10; 
SELECT * FROM t_cfg_metemodel LIMIT 10; 
SELECT * FROM t_cfg_metemodel_detail LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_name = 'UPS配电' and precinct_id = '01-01-08-04-07-01-01';

INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) VALUES ('1', '00001006000000200000', 'UPS配电', '01-01-08-04-07-01-01', 8, NULL, 000, '00001008000000016602', 11, NULL, 9, 1, NULL, '100100000000009', 1617, 1, NULL, NULL, NULL, '2025-08-12 18:11:53', NULL, NULL, NULL, NULL, '中兴力维', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 10106425, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, 0, '2025-08-12 17:04:32', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

SELECT * FROM t_cfg_device WHERE device_id like '000010060000002000%'

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-08-04-07-01-01'



SELECT * FROM 	energy_cabinet_column LIMIT 10;
SELECT * FROM 	energy_cabinet_column WHERE id = '94219d809faa4bf9b6dd7d41c3bfdb0c'

SELECT * FROM energy_cabinet WHERE id = '14554ea75d774c92b11be449c5b28c50'


SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_device WHERE precinct_id like '01-01-08-04-15-G97-02%' AND device_name LIKE "UPS配电%"



SELECT * FROM 	energy_cabinet_column WHERE id = '08da2f29258941b48b2f4480f7ba2c01'
SELECT * FROM energy_cabinet WHERE cabinet_name = '222'
