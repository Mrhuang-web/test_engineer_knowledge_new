SELECT * FROM t_scheduled_task;

SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '百色测试数据县八洋小区基站无线机房';
SELECT * FROM t_cfg_device WHERE precinct_id = '01-07-05-01-01-01';

SELECT * FROM t_cfg_device WHERE device_name = '山东力创交流智能电表1' AND precinct_id = '01-07-05-01-01-01';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000085120';
SELECT * FROM t_cfg_metemodel where device_type = '92' LIMIT 10;


SELECT * FROM t_cfg_device WHERE device_name = '高压配电' AND precinct_id = '01-07-05-01-01-01';
SELECT * FROM t_cfg_metemodel where device_type = '1' LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000085118';

SELECT * FROM t_cfg_device WHERE device_name = '低压交流配电' AND precinct_id = '01-07-05-01-01-01';
SELECT * FROM t_cfg_metemodel where device_type = '2' LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000085120';




green_smart_building_buildings      		绿色智慧楼宇-建筑基础信息表
green_smart_building_electricity_meters     绿智楼宇建筑电表信息表
green_smart_building_electricity_day		日用电量表
green_smart_building_energy_statistics		绿色智能建筑能源消耗统计表
t_scheduled_task


SELECT * FROM green_smart_building_buildings;   
SELECT * FROM green_smart_building_electricity_meters;
SELECT * FROM green_smart_building_electricity_day;
INSERT INTO `green_smart_building_electricity_day` (`meter_id`, `r_day`, `power`) 
VALUES ('00771006000002943028_092316_1', '20251208',10.91);

SELECT * FROM green_smart_building_energy_statistics;

INSERT INTO `t_cfg_metemodel_detail` (`model_id`, `mete_id`, `mete_kind`, `device_type`, `mete_code`, `mete_index`, `mete_no`, `up_mete_id`, `raw_mete_code`, `mete_desc`) VALUES ('00001008000000085120', '71001300000000250311', 1, 92, '092316', NULL, 1, '正向有功电能', '60092-00-092316', NULL);







SELECT building.meter_id meterId, building.precinct_id precinctId, room.precinct_name relatedRoom, site.precinct_name relatedSite, site.precinct_id siteId, city.precinct_name cityName, city.precinct_id cityId, building.device_id deviceId, device.device_name relatedDevice, building.mete_code meteCode, mete.up_mete_id realSignalName, building.signal_number signalNumber, building.building_id buildingId, building1.build_name buildName, building.installation_location installationLocation, building.point_type pointType, building.data_upload_method dataUploadMethod, building.installation_type installationType, building.created_at createdAt, building.updated_at updatedAt 
FROM green_smart_building_electricity_meters building 
LEFT  JOIN green_smart_building_buildings building1  ON building.building_id = building1.building_id 
LEFT  JOIN t_cfg_device device  ON building.device_id = device.device_id 
LEFT  JOIN `t_cfg_metemodel_detail` mete  ON mete.model_id= device.device_model  AND mete.mete_no=building.signal_number  AND mete.mete_code=building.mete_code 
LEFT  JOIN t_cfg_precinct room  ON building.precinct_id = room.precinct_id  AND room.precinct_kind = '5' 
LEFT  JOIN t_cfg_precinct build  ON build.precinct_id = room.up_precinct_id  AND build.precinct_kind = 3 
LEFT  JOIN t_cfg_precinct site  ON site.precinct_id =  IFNULL(build.up_precinct_id, room.up_precinct_id) 
LEFT  JOIN t_cfg_precinct city  ON 
LEFT(room.precinct_id,8) = city.precinct_id 
WHERE 1=1  AND (building.precinct_id  LIKE  CONCAT('01-07-05-01-01','%'))  AND (building.precinct_id  IN (
LEFT('01-07-19-04',8), 
LEFT('01-07-19-03',8), 
LEFT('01-07-19-03',8))  OR (building.precinct_id  LIKE  CONCAT(
LEFT('01-07-06',8),'%')  OR building.precinct_id  LIKE  CONCAT(
LEFT('01-07',8),'%')  OR building.precinct_id  LIKE  CONCAT(
LEFT('01-07-10',8),'%')  OR building.precinct_id  LIKE  CONCAT(
LEFT('01-07-12',8),'%')  OR building.precinct_id  LIKE  CONCAT(
LEFT('01-07-16',8),'%')  OR building.precinct_id  LIKE  CONCAT(
LEFT('01-07-05',8),'%'))) 
ORDER  BY building.created_at  DESC 
LIMIT 15;




SELECT  * FROM green_smart_building_energy_statistics;



# 查看有三种设备类型的站点信息
SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';

SELECT 
	device.device_id,
	device.device_name,
	device.device_model,
	device.precinct_id,
	room.precinct_name,
	site.precinct_name,
	city.precinct_name,
	province.precinct_name 
	FROM t_cfg_device device
	JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id AND CHAR_LENGTH(room.precinct_id) < 18
	JOIN t_cfg_precinct site ON room.up_precinct_id = site.precinct_id
	JOIN t_cfg_precinct county ON site.up_precinct_id = county.precinct_id 
	JOIN t_cfg_precinct city ON county.up_precinct_id = city.precinct_id  
	JOIN t_cfg_precinct province ON city.up_precinct_id = province.precinct_id  
	WHERE 
		device.device_type IN (92,1,2) LIMIT 1000;

SELECT 
	device.device_id,
	device.device_name,
	device.device_model,
	device.precinct_id,
	room.precinct_name,
	building.precinct_name,
	site.precinct_name,
	city.precinct_name,
	province.precinct_name 
	FROM t_cfg_device device
	JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id AND CHAR_LENGTH(room.precinct_id) > 18
	JOIN t_cfg_precinct building ON room.up_precinct_id = building.precinct_id
	JOIN t_cfg_precinct site ON building.up_precinct_id = site.precinct_id
	JOIN t_cfg_precinct county ON site.up_precinct_id = county.precinct_id 
	JOIN t_cfg_precinct city ON county.up_precinct_id = city.precinct_id  
	JOIN t_cfg_precinct province ON city.up_precinct_id = province.precinct_id  
	WHERE 
		device.device_type IN (92,1,2) LIMIT 1000;
		
SELECT * FROM t_cfg_precinct WHERE device_model = '00001008000000123668';		
SELECT * FROM t_cfg_device WHERE device_model = '00001008000000123668';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000123668';


SELECT * FROM t_cfg_device WHERE device_id = '00161006000000023354';

SELECT * FROM green_smart_building_buildings WHERE build_name != '楼宇名称1233';
SELECT * FROM green_smart_building_electricity_meters WHERE building_id != '建筑ID213';









# url 越权
SELECT * FROM t_cfg_filter_file_auth;
SELECT * FROM t_cfg_auth_uri_config;
INSERT INTO `t_cfg_auth_uri_config` (`id`, `type`, `uri`, `create_time`, `is_del`) 
VALUES (16, '1', 'v1/greenSmart/common/exportLog', '2025-12-11 16:44:32', 0);


001328
SELECT * FROM t_cfg_device WHERE device_name LIKE "%高压进线柜%" LIMIT 100;


SELECT * FROM t_cfg_metemodel_detail where mete_code = '001328' LIMIT 10;



# 实时监控查看哪些有对应测点数据(这个语法用不了，直接到实时监控或是用电关系里面找即可)
	SELECT room.precinct_name,device.* FROM t_cfg_monitordevice monitor
		JOIN t_cfg_device device ON monitor.device_id = device.device_id AND device.device_type = '1'
		JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
		LIMIT 100;


# sftp 捞数据
	get Building_GX_202511.csv.gz /tmp/tmp/
	get Meter_GX_202511.csv.gz /tmp/tmp/
	get OtherEnergy_GX_202511.csv.gz /tmp/tmp/
	get MeterPowerDaily_GX_20251210.csv.gz /tmp/tmp/



{"sftpUser":"sudoroot","sftpPwd":"wccQKPbCmx8@r*6p","sftpIp":"10.1.4.113","sftpPort":22,"sftpPath":"/tmp/dhdata/yyyyMMdd","localDir":"/tmp/","filePrefix" : "MeterPowerDaily_GX_","timeFormat":"yyyyMMdd","fileSuffix" : ".csv","splitChar" : "|","lineSeparator" : "\r\n","timeType" : "1","timeOffset" : -1,"head":"meterId:meter_id, power:power","provinceId":"01-07","batchSize":"500","meteCodes":"2:002330/1:001328/92:092316"}