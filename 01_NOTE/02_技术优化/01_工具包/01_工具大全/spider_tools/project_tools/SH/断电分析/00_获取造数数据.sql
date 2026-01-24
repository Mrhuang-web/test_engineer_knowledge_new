# 创建机柜列需要的前置数据集
SELECT
	site.precinct_name,
	building.precinct_name,
	room.precinct_name,
	room.precinct_id
from t_cfg_precinct room
    left join t_cfg_precinct building on room.up_precinct_id = building.precinct_id
    left join t_cfg_precinct site on building.up_precinct_id = site.precinct_id
where
    building.precinct_id = '01-01-08-04-16-01';


# 创建机柜
补充


# 获取机柜
SELECT
    cabinet.id
FROM energy_cabinet cabinet
	 LEFT JOIN t_cfg_precinct room ON cabinet.precinct_id = room.precinct_id
	 left join t_cfg_precinct building on room.up_precinct_id = building.precinct_id
WHERE room.precinct_id = '01-01-08-04-16-01'