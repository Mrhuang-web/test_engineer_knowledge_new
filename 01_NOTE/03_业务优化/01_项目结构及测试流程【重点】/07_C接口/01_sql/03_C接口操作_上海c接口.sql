SELECT * FROM t_cfg_site_mapping GROUP BY mapping_name HAVING COUNT(*) >= 2

SELECT * FROM t_cfg_cserverinfo
SELECT * FROM t_cfg_cserverinfo_mapping

INSERT INTO `t_cfg_cserverinfo` (`lsc_id`, `lsc_name`, `csvrip`, `csvrport`, `clogusrname`, `clogusrpwd`, `dbtype`, `dbsvrip`, `dbsvrport`, `dbname`, `dblogname`, `dblogpwd`, `access_device_id`, `protocol_id`) 
VALUES ('331', 'C接口接入上海', '10.1.203.38', 8033, 'admin', 'Dh@159_dev', 6, '10.1.203.120', 3306, 'cinterdb_400', 'root', 'Fsdy9KXkt1OqngvuwduKIHGCf2uDVGBKSj+Gq9JPkM8=', '00001006000000755298', 400);


INSERT INTO t_cfg_cserverinfo_mapping
(precinct_id, precinct_name, status, url, url_bak, server_name, lsc_id, lsc_name)
VALUES('01-25', '上海接入B08', 0, 'http://10.1.203.121:8282/v1/cinterface/syncBycommand', NULL, 'cinterface-service-B08', 331, '上海接入B08接入');




INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (14, '广东-卓望', '潮州市', '饶平县', 2, NULL, '01-01-23-02-10', 'LSC400测试机楼2006', 'LSC400测试机楼2006', NULL);

INSERT INTO `t_cfg_site_mapping` (`id`, `province_name`, `city_name`, `area_name`, `site_type`, `interface_type`, `lsc_id`, `lsc_name`, `mapping_name`, `mark`) 
VALUES (15, '广东-卓望', '潮州市', '饶平县', 2, NULL, '01-01-23-02-11', 'LSC400测试机楼2007', 'LSC400测试机楼2007', NULL);


SELECT * FROM t_cfg_precinct where precinct_name = "上海"

# ----------------------------------------------------------------------
SELECT * FROM m_area WHERE siteid = '244'  LIMIT 100;
SELECT * FROM m_site WHERE siteid = '244' LIMIT 100;
SELECT * FROM m_device LIMIT 100;
SELECT * FROM m_device WHERE siteid = '244' 

SELECT * FROM m_room WHERE siteid = '244';


SELECT * FROM m_site WHERE SiteName = 'LSC400测试机楼2006'





SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-02-29'


INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广东', '广州市', '白云区', 2, NULL, '01-01-17-02-29', '广州白云区矮岭西街一巷16号', '广州白云区矮岭西街一巷16号', NULL);


SELECT * FROM t_cfg_site_mapping


INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广东', '汕头市', '濠江区', 1, NULL, '01-01-08-04-11', '黄某某_上海定制4', 'C接口接入号', NULL);







SELECT * FROM t_cfg_cserverinfo

SELECT * FROM t_cfg_cserverinfo_mapping
SELECT * FROM m_area WHERE siteid = '244'  LIMIT 100;
SELECT * FROM m_site WHERE siteid = '244' LIMIT 100;
