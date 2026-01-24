SELECT * FROM zz_to_rm_rm_device;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-03-01-26-01';

SELECT MAX(siteid) FROM m_site LIMIT 10;
SELECT * FROM m_site LIMIT 10;
SELECT * FROM m_room WHERE siteid IN ('2045','2046','2047');
SELECT * FROM m_device WHERE siteid IN ('2045','2046','2047');
SELECT * FROM m_signal WHERE deviceid = '68949';


DELETE FROM m_site WHERE siteid IN ('2045','2046','2047','2048');
DELETE FROM m_room WHERE siteid IN ('2045','2046','2047','2048');
DELETE FROM  m_device WHERE siteid IN ('2045','2046','2047','2048');


SELECT * FROM t_cfg_site_mapping 

INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (7121114, '贵州-接入', '安顺市', '紫云苗族布依族自治县', 1, 1, '01-08-08-04-07-01', '贵州_数据中心_楼栋1', '贵州_数据中心_楼栋1', 'siteManage2034');

INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (7121115, '贵州-接入', '安顺市', '紫云苗族布依族自治县', 1, 1, '01-08-08-04-07-02', '贵州_数据中心_楼栋2', '贵州_数据中心_楼栋2', 'siteManage2034');

INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (7121116, '贵州-接入', '安顺市', '紫云苗族布依族自治县', 1, 1, '01-08-08-04-07-03', '贵州_数据中心_楼栋3', '贵州_数据中心_楼栋1', 'siteManage2034');

INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (7121117, '贵州-接入', '安顺市', '紫云苗族布依族自治县', 2, 1, '01-08-08-04-08', '贵州_通信枢纽楼_拓扑', '贵州_通信枢纽楼_拓扑', 'siteManage2034');
