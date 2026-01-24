select id, site_id as siteId, device_name as collectorName, inet_ntoa(ip) as collectorIp, room_name as collectorRoomName from t_cfg_ip where 1=1 and device_name is not null and device_type = 6 

select * from t_zz_space_resources  where int_id = 'SITE-ff80808155de01c501560093ff3e0030';
select * from t_cfg_precinct where precinct_id = '01-07-16-05-04';



SELECT * FROM t_alert_network_accept_flow;
delete from t_alert_network_accept_flow where work_code = 'CS20251124001';
SELECT * FROM t_alert_network_accept_device;
SELECT * FROM t_alert_network_accept_data;
SELECT * FROM t_alert_network_accept_fsu;