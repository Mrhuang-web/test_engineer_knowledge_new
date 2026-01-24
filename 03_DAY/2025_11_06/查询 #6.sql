SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-04-03%' AND precinct_kind = 3


SELECT * FROM t_cfg_dict WHERE col_name = 'building_type'



SELECT * FROM t_zz_power_specialty LIMIT 10
SELECT * FROM t_zz_power_specialty where power_device_id = '6' LIMIT 10


SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_dict WHERE dict_note = 'FSU';
SELECT * FROM zz_resource_device_analys;


SELECT * FROM t_zz_power_device LIMIT 10
SELECT * FROM t_cfg_ip
SELECT * FROM t_cfg_ip_process_record




SELECT * FROM t_zz_power_device_sys LIMIT 10



SELECT * FROM t_zz_power_device WHERE device_subclass = 'FSU' LIMIT 1000
SELECT * FROM t_zz_power_device WHERE device_type = '监控设备' and zh_label LIKE "柳州%" LIMIT 1000


SELECT * FROM t_zz_power_device WHERE 
# device_subclass = 'FSU' AND 
related_site = '07977e6db645423bb8b61a3fd1ccb542' LIMIT 1000

SELECT * FROM t_zz_power_device LIMIT 10


SELECT * FROM t_zz_space_resources LIMIT 10
SELECT * FROM t_zz_space_resources where related_site = 'SITE-77003339' LIMIT 10
SELECT * FROM t_zz_space_resources where int_id = '441000000000008079458722' LIMIT 10

SELECT * FROM t_zz_space_resources 
where related_site IN (SELECT related_site FROM t_zz_power_device WHERE device_type = '监控设备' ) LIMIT 10

SELECT * FROM t_zz_site_property LIMIT 10





# precinct_id:   01-07-12-04-76-01
# int_id         ROOM-cd86bd0e8d9342bba2f7950e47544d9c
# related_site   SITE-b424dcfb49064d7d8334a0118fe289ff
SELECT * FROM t_zz_space_resources where precinct_id is not null LIMIT 10
SELECT * FROM t_zz_space_resources where precinct_id is not NULL AND space_type = 102 LIMIT 10


# res_code     441100000000067835886082
# related_site 441000000000008079458722
# related_room 441000000000008004698902
SELECT * FROM t_zz_power_device WHERE device_subclass = 'FSU' LIMIT 1000







