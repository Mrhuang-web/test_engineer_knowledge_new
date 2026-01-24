INSERT INTO t_cfg_cserverinfo
(lsc_id, lsc_name, csvrip, csvrport, clogusrname, clogusrpwd, dbtype, dbsvrip, dbsvrport, dbname, dblogname, dblogpwd, access_device_id, protocol_id)
VALUES(543, '广西测试环境接入_hjj', '10.1.203.38', 5234, 'hyzomc', 'hyzomc@2023 ', 6, '10.1.203.38', 3306, 'root', 'cinterdb_400', '数据库密码', '1', 400);




SELECT * FROM t_cfg_site_mapping;

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES
('广西-卓望', '汕头市', '濠江区', 2, NULL, '01-07-22-01-01', '汕头数据中心一号楼', '汕头数据中心一号楼', NULL),
('广西-卓望', '汕头市', '濠江区', 2, NULL, '01-07-22-01-02', '汕头数据中心二号楼', '汕头数据中心二号楼', NULL),
('广西-卓望', '汕头市', '濠江区', 2, NULL, '01-07-22-01-03', '汕头核心机楼', '汕头核心机楼', NULL),
('广西-卓望', '汕头市', '濠江区', 2, NULL, '01-07-22-01-04', '汕头传输节点', '汕头传输节点', NULL),
('广西-卓望', '汕头市', '濠江区', 2, NULL, '01-07-22-01-05', '汕头通讯基站', '汕头通讯基站', NULL);



SELECT * FROM t_cfg_cserverinfo
SELECT * FROM t_cfg_cserverinfo_mapping
SELECT * FROM m_area;
SELECT * FROM m_site;
SELECT * FROM m_room;


SELECT * FROM t_cfg_precinct WHERE precinct_name = '汕头核心机楼机房1';



