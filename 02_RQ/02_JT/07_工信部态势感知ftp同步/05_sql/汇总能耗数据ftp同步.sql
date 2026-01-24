# 定时任务表
select * from t_scheduled_task;

# 定位数据中心
SELECT * FROM t_cfg_dict WHERE col_name = 'precinct_kind'; 
SELECT * FROM t_cfg_dict WHERE dict_note = '数据中心';
SELECT * FROM t_cfg_precinct WHERE precinct_kind = 2;
SELECT * FROM t_cfg_site WHERE site_type = 1;

# 查询现有数据中心
SELECT a.precinct_name,b.* FROM t_cfg_precinct a INNER JOIN t_cfg_site b ON a.precinct_id = b.site_id
WHERE a.precinct_kind =2 AND b.site_type = 1 GROUP BY b.site_id;

# 查询属于投产初期的数据中心 的机楼则不纳入统计
SELECT a.precinct_name,c.* FROM t_cfg_precinct a INNER JOIN t_cfg_site b ON a.precinct_id = b.site_id
INNER JOIN energy_access_specimen_site c ON c.site_id = b.site_id 
WHERE a.precinct_kind =2 AND b.site_type = 1 GROUP BY c.site_id;

# 最终计算数据中心站点 79 - 11 = 68