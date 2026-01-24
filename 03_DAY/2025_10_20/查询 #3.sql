select * from t_zz_power_specialty where zh_label = '百色测试数据to传输节点';



SELECT resource_device_type_name,device_type_name,device_sub_type_name 
FROM overdue_device_detail group by device_type_name,device_sub_type_name LIMIT 200

SELECT * from t_alter_network_accept_model;
SELECT * from t_alert_network_accept_flow;
SELECT * from t_alert_network_accept_fsu;
SELECT * from t_alert_network_accept_device;
SELECT * from t_alert_network_accept_data;


SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-16-05-04-05';
SELECT * FROM t_cfg_dict WHERE col_name = 'mete_kind';
SELECT * FROM t_cfg_device WHERE device_id = '00781006000003077481';
SELECT * FROM t_cfg_metemodel_detail WHERE device_type = 6 AND  model_id = '00001008000000003754';
006001\006301\006101\006206\006401
SELECT * FROM t_cfg_metemodel_detail WHERE device_type = 6 AND  model_id = '00001008000000003754' AND mete_code IN
(006001,006301,006101,006206,006401); 
spider