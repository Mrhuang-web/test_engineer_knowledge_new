SELECT * FROM t_scheduled_task;
SELECT * FROM  zz_data_sync_info;
SELECT order_id,order_name,model_name_cn,model_name_en,TABLE_NAME,batch_num FROM zz_data_sync_info
WHERE TABLE_NAME IS NOT NULL;
UPDATE zz_data_sync_info SET batch_num = '20250723000000' WHERE batch_num = '20251210000000';


SELECT * FROM  dim_zz_data_sync_info;

SELECT COUNT(1) FROM ods_zz_site_property;
SELECT COUNT(1) FROM ods_zz_site_property GROUP BY batch_num;
SELECT batch_num FROM ods_zz_site_property GROUP BY batch_num;
SELECT * FROM ods_zz_site_property order by flow_time desc LIMIT 1000;
SELECT * FROM ods_zz_site_property where res_code = '-1011527355' LIMIT 10;
SELECT res_code,COUNT(batch_num) FROM ods_zz_site_property GROUP BY res_code;
TRUNCATE TABLE ods_zz_site_property;
SELECT 222367+641863; # 20251210   864230


SELECT COUNT(1) FROM ods_zz_site;
SELECT batch_num,COUNT(1) FROM ods_zz_site GROUP BY batch_num;
SELECT * FROM ods_zz_site LIMIT 10;
SELECT batch_num FROM ods_zz_site GROUP BY batch_num;
SELECT flow_time FROM ods_zz_site GROUP BY flow_time;
SELECT flow_time FROM ods_zz_site GROUP BY flow_time;
SELECT * FROM ods_zz_site order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_site;
SELECT 541040+142147+208204+21513+64724+800520+40864+125892+1789405+85213+32603+253269+54469+1833197+103890+
31335+151539+213305+167074+318605+344206+39948+158158+363747+20392+652545+68584+107465+197989+81247 
# 39   9013089



SELECT COUNT(1) FROM ods_zz_room_property;
SELECT * FROM ods_zz_room_property order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_room_property;
SELECT 397832+913648
# 1311480



SELECT COUNT(1) FROM ods_zz_room;
SELECT * FROM ods_zz_room order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_room;
SELECT 546106 +200147 +2329092 +201126 +23756 +338603 +805887 + 141177 + 1218877  + 31986 
+ 106496 + 221882 + 39324 + 88053 + 67901  + 179757 + 88809 + 55046  + 352570  + 155936 +
251497 + 1956252 + 145063 + 170744 + 227999 + 82590 
# 10026676



SELECT COUNT(1) FROM ods_zz_ldhink_pe_in;
SELECT * FROM ods_zz_link_pe_in order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_link_pe_in;
SELECT 8972  +99639  +50850  +64835 +42754 +46335 +8404 +8482+182446 +82876 +411564 +56170 +16985 
+385214 +26592 +75978 +37772 +20674 +12398 +153071 +5310 +2918 +24838 +63271 +44964 +23566 +
151450 +161166 +17276 +16177 +11754 
# 2314701




SELECT COUNT(1) FROM ods_zz_irms_site_map;
SELECT * FROM ods_zz_irms_site_map order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_irms_site_map;
SELECT 1553 




SELECT COUNT(1) FROM ods_zz_irms_rom_map;
SELECT * FROM ods_zz_irms_rom_map order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_irms_rom_map;
SELECT 26277 



SELECT COUNT(1) FROM ods_zz_irms_dc_map;
SELECT * FROM ods_zz_irms_dc_map order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_irms_dc_map;
SELECT 66


SELECT COUNT(1) FROM ods_zz_device_ups;
SELECT * FROM ods_zz_device_ups order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_ups;
SELECT 166981 



SELECT COUNT(1) FROM ods_zz_device_transform_device;   -- 缺失文件？
SELECT * FROM ods_zz_device_transform_device order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_transform_device;
SELECT 68209 



SELECT COUNT(1) FROM ods_zz_device_transform;
SELECT * FROM ods_zz_device_transform order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_transform;
SELECT 71146  



SELECT COUNT(1) FROM ods_zz_device_switch_power;
SELECT * FROM ods_zz_device_switch_power order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_switch_power;
SELECT 933002 + 326010 
# 1259012



SELECT COUNT(1) FROM ods_zz_device_smart_meter;
SELECT * FROM ods_zz_device_smart_meter order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_smart_meter;
SELECT 120897 + 344902 
# 465799



SELECT COUNT(1) FROM ods_zz_device_power_monitor;
SELECT * FROM ods_zz_device_power_monitor order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_power_monitor;
SELECT 30708  + 52611 + 137257 +3306 +10634 +40207 +207760 +18481 +126603 +16576 +54033 +3900 
+ 27507 +12114 +68611 +1626 +76404 +64438 +73873 +130535 +42446 +100353 +141286 +29933 +317316 
+119189 +29791 +176994 +26550 +40758 +295985  
# 2477785




SELECT COUNT(1) FROM ods_zz_device_power_generation;
SELECT * FROM ods_zz_device_power_generation order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_power_generation;
SELECT 49167




SELECT COUNT(1) FROM ods_zz_device_other;
SELECT * FROM ods_zz_device_other order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_other;
SELECT 90937 



SELECT COUNT(1) FROM ods_zz_device_low_dc_distribution;
SELECT * FROM ods_zz_device_low_dc_distribution order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_low_dc_distribution;
SELECT  262769



SELECT COUNT(1) FROM ods_zz_device_low_ac_distribution;
SELECT * FROM ods_zz_device_low_ac_distribution order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_low_ac_distribution;
SELECT  669385 +223813 
# 893198


# 高压直流电源
SELECT COUNT(1) FROM ods_zz_device_high_power;
SELECT * FROM ods_zz_device_high_power order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_high_power;
SELECT 3943 


# 高压配电
SELECT COUNT(1) FROM ods_zz_device_high_distribution;
SELECT * FROM ods_zz_device_high_distribution order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_high_distribution;
SELECT 50160 



SELECT COUNT(1) FROM ods_zz_device_high_dc_distribution;
SELECT * FROM ods_zz_device_high_dc_distribution order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_high_dc_distribution;
SELECT 14495 




SELECT COUNT(1) FROM ods_zz_device_energy_save;
SELECT * FROM ods_zz_device_energy_save order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_energy_save;
SELECT 34034
# 3次了-102102


SELECT COUNT(1) FROM ods_zz_device_battery;
SELECT * FROM ods_zz_device_battery order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_battery;
SELECT 53252 + 6781 +13919 +52874 +87035 +22744 +82620 +141899 +133154 +68963 +11207 +3927 +111328 +18725 +50230 
+36376 +43347 +147405 +18949 +69184 +3891 +120626 +15684 +253711 +21766 +55199 +27433 +27686 +56604 +9535 
# 1766054




SELECT COUNT(1) FROM ods_zz_device_air;
SELECT * FROM ods_zz_device_air order by flow_time desc LIMIT 10;
TRUNCATE TABLE ods_zz_device_air;
SELECT 12994  + 42753 +66509 +33666 +28304 +34243 +85767 +34132 +38270 +105304 +24935 +29172 + 59604 
+5964 +53247 +36859 +58532 +3665 +18857 +86464 +41393 +1093 +77779 +19132 +160241 +50395 
+29398 +189966 +29250 +92968 
# 1550856