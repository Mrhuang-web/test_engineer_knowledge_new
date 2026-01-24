# 筛选设备类型
SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';

SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_type = 2 LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail where mete_code = '002307' LIMIT 10;


# 构建机房下有设备，设备测点模板有测点
SELECT * FROM t_cfg_device WHERE device_type = 2 AND device_id = '00531006000002591949';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000003521';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11-02-02-01';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11-02-02';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11-02';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11';



# 直接找已有设备看
SELECT * FROM t_cfg_device WHERE device_name = '1#高压配电-1#操作电源_1F';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11-02-02-11';

SELECT * FROM t_cfg_device WHERE device_name = '1#高压配电-1#操作电源_1F';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-11-02-02-11';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000003521';
SELECT * FROM t_cfg_metemodel_detail WHERE device_type = 1
