SELECT * FROM t_cfg_dict WHERE col_name = 'mete_kind';
SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_metemodel_detail WHERE device_type = 2 LIMIT 10;

SELECT * FROM t_cfg_mete WHERE mete_code LIKE "002%" LIMIT 40;


SELECT * FROM t_device_type_mapped;



SELECT device_type FROM t_zz_power_device group by device_type LIMIT 30;
SELECT device_type FROM t_zz_power_specialty group by device_type LIMIT 30;






SELECT *
FROM (
    SELECT res_code,
           device_id,
           zh_label,
           lifecycle_status,
           device_type,
           related_room,
           related_site,
           device_subclass
    FROM t_zz_power_device t
    WHERE 1 = 1
      AND t.lifecycle_status = '退网'
) device
LEFT JOIN t_zz_space_resources zz_room
       ON zz_room.int_id = device.related_room
      AND zz_room.space_type = 102
      AND zz_room.related_site = device.related_site
LEFT JOIN t_zz_space_resources zz_site
       ON zz_room.related_site = zz_site.int_id
LEFT JOIN t_cfg_precinct room
       ON room.precinct_id = zz_room.precinct_id
LEFT JOIN t_cfg_precinct build
       ON room.up_precinct_id = build.precinct_id
      AND build.precinct_kind = 3
      AND build.isdel = '0'
LEFT JOIN t_cfg_precinct site
       ON IFNULL(build.up_precinct_id, room.up_precinct_id) = site.precinct_id
      AND site.precinct_kind = 2
      AND site.isdel = '0'
LEFT JOIN t_cfg_precinct area
       ON area.precinct_id = LEFT(room.precinct_id, 11)
LEFT JOIN t_cfg_precinct city
       ON city.precinct_id = LEFT(room.precinct_id, 8)
LEFT JOIN t_cfg_site site_type
       ON site_type.site_id = site.precinct_id
LEFT JOIN t_cfg_dict p
       ON p.dict_code = site_type.site_type
      AND p.col_name = 'site_type'
WHERE room.precinct_kind = 5
  AND room.isdel = '0';
  

SELECT * FROM t_zz_power_device  where res_code = '2f3d8b239d80410c9a643d7641934e64' LIMIT 10;

SELECT * FROM t_al


SELECT * FROM t_cfg_precinct WHERE precinct_name = '梧州测试数据区工业园生产楼二楼电力机房';
# 原始model：00001008000000003990  ，  修改程00001008000000003754
SELECT * FROM t_cfg_device WHERE precinct_id = '01-07-16-05-04-05' AND device_name = '维谛技术分立开关电源7/7';
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_mete WHERE mete_name = '回风温度' AND device_type = 6;
SELECT * FROM t_cfg_mete WHERE mete_code LIKE "006%";


SELECT * FROM t_cfg_metemodel WHERE model_id = '00001008000000003754'
SELECT * FROM t_cfg_metemodel_detail LIMIT 10

SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000003754'