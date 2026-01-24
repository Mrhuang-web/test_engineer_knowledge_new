# 能耗管理
# 01-07
SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%0517%";
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07'

SELECT * FROM m_area;
SELECT * FROM m_site;
SELECT * FROM m_room;

SELECT * FROM T_CFG_DICT WHERE DICT_NOTE = '数据中心'
SELECT * FROM T_CFG_DICT WHERE col_name IN ('station_type','site_level','site_type')


SELECT * FROM t_cfg_cserverinfo


INSERT INTO t_cfg_cserverinfo
(lsc_id, lsc_name, csvrip, csvrport, clogusrname, clogusrpwd, dbtype, dbsvrip, dbsvrport, dbname, dblogname, dblogpwd, access_device_id, protocol_id)
VALUES(543, '广西测试环境接入_hjj', '10.1.203.38', 5234, 'hyzomc', 'hyzomc@2023 ', 6, '10.1.203.38', 3306, 'root', 'cinterdb_400', 'G$SGp!8L3O', '1', 400);



select * from t_cfg_site_mapping

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广西-卓望', '广州市', '天河区', 4, NULL, '01-07-21-01-01-05', 'HJJ通讯基站', 'HJJ通讯基站', NULL);

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广西-卓望', '广州市', '天河区', 3, NULL, '01-07-21-01-01-04', 'HJJ传输节点', 'HJJ传输节点', NULL);

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广西-卓望', '广州市', '天河区', 2, NULL, '01-07-21-01-01-03', 'HJJ核心机楼', 'HJJ核心机楼', NULL);

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广西-卓望', '广州市', '天河区', 1, NULL, '01-07-21-01-01-02', 'HJJ数据中心四号楼', 'HJJ数据中心四号楼号', NULL);

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('广西-卓望', '广州市', '天河区', 1, NULL, '01-07-21-01-01-01', 'HJJ数据中心三号楼', 'HJJ数据中心三号楼', NULL);



