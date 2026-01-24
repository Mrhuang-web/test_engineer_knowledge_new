SELECT COUNT(0)
FROM (
SELECT county_id AS regionId, COUNT(*) AS totalConvergenceSites, COUNT(CASE WHEN cutin_date > '2025-01-01' THEN 1 END) AS totalSitesOverDate, COUNT(CASE WHEN cutin_date > '2025-01-01' AND mains_nature = '市电直供' THEN 1 END) AS directPowerSitesOverDate, COUNT(CASE WHEN cutin_date > '2025-01-01' AND mains_nature = '市电转供' THEN 1 END) AS transferPowerSitesOverDate, COUNT(CASE WHEN cutin_date > '2025-01-01' AND (mains_nature IS NULL OR mains_nature NOT IN ('市电直供', '市电转供')) THEN 1 END) AS unknownPowerSupplySitesOverDate
FROM zz_to_rm_agg_convergence_site
WHERE 1 = 1 AND province_id = 440000 AND city_id = 440300 AND county_id = 440305
GROUP BY county_id
HAVING county_id IS NOT NULL) AS zasite
LEFT JOIN t_cfg_precinct tcp ON zasite.regionId = tcp.area_code
WHERE tcp.precinct_kind = 1


SELECT * FROM zz_to_rm_agg_convergence_site group by update_time desc LIMIT 100;
DELETE FROM zz_to_rm_agg_convergence_site
SELECT * FROM zz_audit_summary_site LIMIT 10;


SELECT * FROM zz_to_rm_agg_convergence_site WHERE province_id = '440000';


# 原始批次：20250507
SELECT * FROM zz_data_sync_info
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-11'

SELECT * FROM zz_to_rm_agg_convergence_site;


SELECT 
	special.zh_label,
	resource.zh_label,
	resource.precinct_id,
	resource.related_site,
	site.precinct_id site,
	room.precinct_id room
FROM t_zz_power_specialty special
	JOIN t_zz_space_resources resource ON special.res_code = resource.int_id AND resource.precinct_id IS NOT NULL 
	left JOIN t_cfg_precinct site ON site.precinct_id = resource.precinct_id AND resource.space_type = 101
	LEFT JOIN t_cfg_precinct room ON room.precinct_id = resource.precinct_id AND resource.space_type = 102

 
 
 
 



SELECT 
	special.zh_label,
	resource.zh_label,
	resource.precinct_id,
	resource.related_site,
	site.precinct_id site,
	room.precinct_id room,
	ip.*
FROM t_zz_power_specialty special
	JOIN t_zz_space_resources resource ON special.res_code = resource.int_id AND resource.precinct_id IS NOT NULL 
	left JOIN t_cfg_precinct site ON site.precinct_id = resource.precinct_id AND resource.space_type = 101
	LEFT JOIN t_cfg_precinct room ON room.precinct_id = resource.precinct_id AND resource.space_type = 102
	LEFT JOIN t_cfg_ip ip ON ip.site_id = resource.int_id








SELECT * FROM zz_to_rm_agg_convergence_site;