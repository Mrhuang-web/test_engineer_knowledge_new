select precinct_id, device_id, power_device_id from t_cfg_device tcd where power_device_id is not null LIMIT 0, 1000;
select precinct_id, device_id, power_device_id from t_cfg_device tcd where power_device_id is not NULL LIMIT 1000,1000;
