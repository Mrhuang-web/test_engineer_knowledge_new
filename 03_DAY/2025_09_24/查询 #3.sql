SELECT * FROM t_cfg_precinct WHERE 


# fsu:20250904102653
# device_id:00001006000000154452                 00001006000000146147   00001006000000154569
# 10.12.7.159   63728

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-09'



SELECT * FROM t_cfg_device WHERE device_id = '00001006000000154452';
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000146147';
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000154531';
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000154569';

SELECT * FROM t_cfg_fsu;
SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000000154452'
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000146147';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154569';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154570';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154571';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154572';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154573';

SELECT * FROM t_cfg_fsu WHERE http_proxy_url = ':3304'

UPDATE t_cfg_fsu  SET http_proxy_url = NULL , ftp_proxy = NULL WHERE http_proxy_url = ':3304'




SELECT * FROM fsu WHERE fsuid = '11011012345';



UPDATE t_cfg_fsu SET http_proxy_url = NULL WHERE device_id = '00001006000000154452';
UPDATE t_cfg_fsu SET ftp_proxy = NULL WHERE device_id = '00001006000000146147';

INSERT INTO t_cfg_nmsdevice
(device_id, service_addr, service_port, up_server_id, web_page, login_state, sip_port, private_service_addr, subnetmask, gateway, rtsp_port, http_port, icpu_summit, imem_summit, isend_summit, irecv_summit, nms_type)
VALUES('00001006000000154452', '127.0.0.1', 3306, NULL, NULL, NULL, NULL, '10.1.203.121', NULL, NULL, NULL, 8099, NULL, NULL, NULL, NULL, 101);







SELECT b.service_addr,b.service_port,b.private_service_addr,b.rtsp_port,a.* FROM t_cfg_device a INNER JOIN t_cfg_nmsdevice b ON a.device_id=b.device_id limit 100;




SELECT * FROM t_cfg_site_mapping


SELECT * FROM t_cfg_mete WHERE mete_code = '015303'













SELECT * FROM t_sync_field_config GROUP BY device_type;
SELECT * FROM t_zz_power_device_20241205 GROUP BY device_type;
SELECT * FROM t_zz_power_specialty GROUP BY device_type;
SELECT * FROM t_zz_power_device_sys GROUP BY device_type;
SELECT * FROM t_zz_power_specialty_bak1112 GROUP BY device_type;


SELECT * FROM zz_resource_device_analys GROUP BY device_type;
SELECT * FROM device_mapping LIMIT 10




SELECT * from sn_zz_ce_device_pe_battery WHERE res_code = 'hjj_test_battery3'
INSERT INTO `sn_zz_ce_device_pe_battery` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `ralated_power_device`, `reted_capacity`, `cell_voltage_level`, `total_monomers_number`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `qr_code_no`, `backup_time`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (11, '2025-08-04 17:40:51', '20250804', 'hjj_test_battery3', '陕西省', '安康市', '白河区', '陕西测试_通信机楼', '陕西测试_通信机楼', '铅酸电池', '开关电源铅酸电池', '陕西测试_通信机楼-铅酸电池', '1', '6-GFM-150M', '南都', 'hjj_test_switch_power2', '150', '12V', '4', '2019-01-10', '2025-01-08', '现网', '黄佳杰', '黄佳杰', '00811006000001788263', '', '', '', '00811006000001788263', '', '');






SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%上海定制6%"



SELECT * FROM t_cfg_device WHERE device_name LIKE "%测试B接口%"
SELECT * FROM t_cfg_device WHERE device_id = '00001006000001531543'

SELECT * FROM t_cfg_fsu 
SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531541'

SELECT * FROM t_cfg_fsu_command_config

SELECT * FROM t_cfg_telesignal 


SELECT * FROM t_cfg_device order by update_time desc LIMIT 50 WHERE device_name LIKE "%2025年%"
SELECT * FROM t_cfg_device WHERE device_code LIKE "%2025092201%"

SELECT * FROM fsu





SELECT precinct_id FROM t_cfg_precinct WHERE precinct_id like '01-01-08-04-15%'


SELECT * FROM energy_cabinet_column  WHERE cabinet_column_number = '7368994381619273728';

delete  FROM t_cfg_precinct where precinct_name LIKE "上海机房%"




SELECT * FROM t_cfg_precinct where precinct_name LIKE "上海楼栋%" ORDER BY precinct_id;


SELECT * FROM (SELECT c.precinct_name AS '站点' ,b.precinct_name AS '楼栋',a.precinct_name AS '机房',a.precinct_id FROM t_cfg_precinct a INNER JOIN t_cfg_precinct b ON a.up_precinct_id = b.precinct_id
INNER JOIN  t_cfg_precinct c ON b.up_precinct_id = c.precinct_id
WHERE a.precinct_name LIKE "上海机房%") e  order BY e.precinct_id DESC ;


SELECT * FROM energy_cabinet_column LIMIT 10;



SELECT * FROM energy_cabinet_column b INNER JOIN (SELECT * FROM (SELECT c.precinct_name AS '站点' ,b.precinct_name AS '楼栋',a.precinct_name AS '机房',a.precinct_id FROM t_cfg_precinct a INNER JOIN t_cfg_precinct b ON a.up_precinct_id = b.precinct_id
INNER JOIN  t_cfg_precinct c ON b.up_precinct_id = c.precinct_id
WHERE a.precinct_name LIKE "上海机房%") e WHERE e.precinct_id = b.precinct_id LIMIT 10;




SELECT * FROM (SELECT c.precinct_name AS '站点' ,b.precinct_name AS '楼栋',a.precinct_name AS '机房',a.precinct_id FROM t_cfg_precinct a INNER JOIN t_cfg_precinct b ON a.up_precinct_id = b.precinct_id
            INNER JOIN  t_cfg_precinct c ON b.up_precinct_id = c.precinct_id
            WHERE a.precinct_name LIKE "上海机房%") e  order BY e.precinct_id DESC ;


SELECT * FROM t_cfg_precinct where precinct_id LIKE "01-01-08-04-15-%"

SELECT precinct_name ,precinct_id FROM t_cfg_precinct WHERE precinct_name like '上海机房%' and precinct_id like '01-01-08-04-15-%';



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









SELECT device_code,device_name FROM  t_cfg_device WHERE device_code LIKE  '%20250922%'


SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail LIMIT 10;

SELECT pt.precinct_name,tcd.* FROM t_cfg_precinct pt INNER JOIN IN (SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-01-08-04-15-%" AND device_name IN ("UPS配电")) AS tcd
pt.precinct_id = tcd.precinct_id




SELECT * from t_cfg_metemodel_detail aa  inner join IN (SELECT pt.precinct_name, tcd.*
FROM t_cfg_precinct pt
INNER JOIN (
    SELECT *
    FROM t_cfg_device
    WHERE precinct_id LIKE '01-01-08-04-15-%'
      AND device_name = 'UPS配电'
) tcd ON pt.precinct_id = tcd.precinct_id) AS tfpd WHERE aa.model_id = device_model;







SELECT  p.precinct_name,
                d.device_model,          -- 一定要透出 model_id
                d.*
        FROM    t_cfg_precinct p
        JOIN    t_cfg_device d
               ON d.precinct_id = p.precinct_id
        WHERE   d.precinct_id LIKE '01-01-08-04-15-%'
          AND   d.device_name = 'UPS配电'



SELECT  mm.*, t.*
FROM    t_cfg_metemodel_detail mm
JOIN   (
        SELECT  p.precinct_name,
                d.device_model,          -- 一定要透出 model_id
                d.*
        FROM    t_cfg_precinct p
        JOIN    t_cfg_device d
               ON d.precinct_id = p.precinct_id
        WHERE   d.precinct_id LIKE '01-01-08-04-15-%'
          AND   d.device_name = 'UPS配电'
       ) AS t
 ON mm.model_id = t.device_model;
 
 
 
 
 
 
 
 
 
 
 
SELECT                 
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
                d.*          -- 这里已含 device_model，别再加一次
        FROM    t_cfg_precinct p
        JOIN    t_cfg_device d
               ON d.precinct_id = p.precinct_id
        WHERE   d.precinct_id LIKE '01-01-08-04-15-%'
          AND   d.device_name = 'UPS配电'
       ) AS t
 ON mm.model_id = t.device_model AND up_mete_id IN 
 ("分路XX相电流Ia","分路XX相电流Ib","分路XX相电流Ic","分路XX相电压Ua","分路XX相电压Ub","分路XX相电压Uc","分路XX有功功率Pa","分路XX有功功率Pb","分路XX有功功率Pc");
 
 
 
 
 
 
 


SELECT cabinet_column_number,cabinet_column_name,id FROM energy_cabinet_column WHERE cabinet_column_name LIKE "测试机柜列%" AND precinct_id = '01-01-08-04-15-G97-02' ORDER BY update_time ASC;


SELECT * FROM energy_cabinet_column 

SELECT * FROM energy_cabinet_column WHERE id = 'b195518f6695406d8222a63038482a13'
SELECT * FROM energy_cabinet WHERE cabinet_column_id = '94219d809faa4bf9b6dd7d41c3bfdb0c';


SELECT * FROM energy_cabinet_poweroutage_current


SELECT * FROM t_cfg_device WHERE device_id LIKE "00713006000000300%" AND precinct_id = '01-01-08-04-15-G97-02'

SELECT * FROM t_cfg_device WHERE device_id = '00713006000000300003'

SELECT * FROM t_cfg_device WHERE precinct_id = '01-01-08-04-13-01-02' 

SELECT * FROM energy_cabinet WHERE precinct_id = '01-01-08-04-13-01-01' 

SELECT * FROM energy_cabinet_attribute_config 


SELECT a.cabinet_name,a.precinct_id,b.* FROM energy_cabinet a INNER JOIN energy_cabinet_attribute_config b
ON b.cabinet_id = a.id 
WHERE b.device_id = '00713006000000154858'
WHERE a.precinct_id = '01-01-08-04-13-01-02'



SELECT * FROM energy_cabinet_poweroutage_current






