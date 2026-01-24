SELECT * FROM t_cfg_dict where col_name = 'building_type' LIMIT 100;
SELECT * FROM t_cfg_dict where dict_note = 'IDC机房' LIMIT 100;
SELECT * FROM energy_project_dict LIMIT 100;
SELECT * FROM energy_common_config;
SELECT * FROM energy_device_mete_202502 LIMIT 100;
SELECT * FROM energy_formula_config;
SELECT * FROM capacity_transformer_manage_electric;
SELECT * FROM t_cfg_device LIMIT 100;
SELECT * FROM energy_cabinet_mete LIMIT 100;
SELECT * FROM t_cfg_metemodel_detail LIMIT 100;
SELECT * FROM cabinet_his_data_analysis LIMIT 100;


# 快速找字段所在表
SELECT 
    c.TABLE_SCHEMA AS '数据库',
    c.TABLE_NAME AS '表名',
    t.TABLE_COMMENT AS '表注释',
    c.COLUMN_NAME AS '字段名',
    c.COLUMN_COMMENT AS '字段注释'  -- 可选添加
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN INFORMATION_SCHEMA.TABLES t
    ON c.TABLE_SCHEMA = t.TABLE_SCHEMA
    AND c.TABLE_NAME = t.TABLE_NAME
WHERE c.COLUMN_NAME LIKE '%device_sum%'
  AND c.TABLE_SCHEMA = 'spider';



# 机房类型查找    IDC机房  -- room_kind 2
SELECT * FROM t_cfg_dict WHERE col_name = "room_kind";
# 用电类别耗电    IDC机房  -- room_kind 2
SELECT * FROM energy_electricity_type_cost_day LIMIT 100;



SELECT * FROM t_cfg_precinct WHERE precinct_name = '广东'






SELECT * FROM  `nmg_spider`.t_cfg_site_mapping

SELECT * FROM  `nmg_spider`.t_cfg_cserverinfo;
