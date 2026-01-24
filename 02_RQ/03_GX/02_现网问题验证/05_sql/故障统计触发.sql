
"说明1：使用的跟隐患统计同一个脚本，都是根据device_code和device_id和metecode来匹配，前面因为device_code为空导致触发失败"
"说明2：接口使用的ip和端口都是一致的，只是路径不同：    10.12.8.147:31454 "
"说明3：特别注意device_code和device_id和metecode来匹配"





-- 测试环境     
-- 百色测试数据县古障2基站无线机房
curl --location --request POST '127.0.0.1:8486/v1/hiddenDanger/faultRule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 246,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002943063",
            "deviceCode": "060200001000001",
            "deviceName": "维谛技术组合开关电源1/1",
            "deviceProperty": "",
            "signalId": "006201",
            "signalName": "均充电压设定值",
            "signalNum": 0,
            "value": 100.169,
            "date": "2025-09-18 00:00:00"
        }
    ]
}'



curl --location --request POST '127.0.0.1:8486/v1/hiddenDanger/faultRule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 26,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002943063",
            "deviceCode": "060200001000001",
            "deviceName": "维谛技术组合开关电源1/1",
            "deviceProperty": "",
            "signalId": "006202",
            "signalName": "浮充电压设定值",
            "signalNum": 0,
            "value": 50.169,
            "date": "2025-09-18 00:00:00"
        }
    ]
}'














-- 故障统计 触发接口
10.12.8.147:31454

curl --location --request POST '10.12.8.147:31454/v1/hiddenDanger/faultRule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 228,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002944984",
            "deviceCode": "150100000000001",
            "deviceName": "科龙柜式空调1",
            "deviceProperty": "",
            "signalId": "015203",
            "signalName": "回风温度设定",
            "signalNum": 0,
            "value": 19.169,
            "date": "2025-09-11 00:00:00"
        }
    ]
}'







# 00771006000002944984

curl --location --request POST '10.188.99.6:8486/v1/hiddenDanger/faultRule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 228,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002944984",
            "deviceCode": "150100000000001",
            "deviceName": "科龙柜式空调1",
            "deviceProperty": "",
            "signalId": "015203",
            "signalName": "回风温度设定",
            "signalNum": 0,
            "value": 19.169,
            "date": "2025-09-11 00:00:00"
        }
    ]
}'








-- 隐患统计 触发接口

-- /v1/hiddenDanger/rule/testRule       

curl --location --request POST '10.188.99.6:8486/v1/hiddenDanger/rule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 228,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002944984",
            "deviceCode": "150100000000001",
            "deviceName": "科龙柜式空调1",
            "deviceProperty": "",
            "signalId": "015203",
            "signalName": "回风温度设定",
            "signalNum": 0,
            "value": 19.169,
            "date": "2025-09-11 00:00:00"
        }
    ]
}'








-- device_code和device_id的查询方式
-- 通过动环t_cfg_device和综资device的device_id关联，然后通过device_id,拿到综资表中改设备id对应device_code
-- 同时还需要注意t_zz_power_device，综资对应设备不是退网的状态

select
            distinct device.device_id deviceId, device.device_name deviceName,
            a3.device_code deviceCode,
            case
                when acid.ralated_power_device is not null then acid.ralated_power_device
                when lithium.ralated_power_device is not null then lithium.ralated_power_device
                else null
                end ralatedPowerDevice,
            case
                when acid.cell_voltage_level is not null then acid.cell_voltage_level
                when lithium.cell_voltage_level is not null then lithium.cell_voltage_level
                else null
                end cellVoltageLevel,
            case
                when acid.total_monomers_number is not null then acid.total_monomers_number
                when lithium.total_monomers_number is not null then lithium.total_monomers_number
                else null
                end totalMonomersNumber,
            case
                when distribution.rated_capacity is not null then distribution.rated_capacity
                when acid.rated_capacity is not null then acid.rated_capacity
                when lithium.rated_capacity is not null then lithium.rated_capacity
                else null
                end ratedCapacity,
            swtitch.signal_output_rated_capacity signalOutputRatedCapacity,
            swtitch.total_rack_match_modules totalRackMatchModules, a3.lifecycle_status lifecycleStatus,
            a3.rated_power ratedPower,
            city.precinct_id cityId, city.precinct_name cityName,
            country.precinct_id countryId, country.precinct_name countryName,
            site.precinct_id siteId, site.precinct_name siteName,
            siteInfo.site_type siteType, siteType.dict_note siteTypeName,
            room.precinct_id roomId, room.precinct_name roomName,
            device.device_type deviceType, deviceType.dict_note deviceTypeName
    from t_cfg_device device
             inner join t_zz_power_device a3 on device.device_id = a3.device_id
             
             inner join t_cfg_dict deviceType on deviceType.col_name = "device_type" and device.device_type = deviceType.dict_code
             inner join t_cfg_precinct room on room.precinct_id = device.precinct_id and room.precinct_kind = 5
             left join t_cfg_precinct building on building.precinct_id = room.up_precinct_id and building.precinct_kind = 3
             inner join t_cfg_precinct site on site.precinct_id = ifnull(building.up_precinct_id, room.up_precinct_id)
             inner join t_cfg_site siteInfo on siteInfo.site_id = site.precinct_id
             inner join t_cfg_dict siteType on siteType.col_name = "site_type" and siteInfo.site_type = siteType.dict_code
             inner join t_cfg_precinct country on site.up_precinct_id = country.precinct_id
             inner join t_cfg_precinct city on country.up_precinct_id = city.precinct_id
             
             left join t_zz_ac_distribution distribution on distribution.res_code = a3.res_code
             left join t_zz_lead_acid_battery acid on acid.res_code = a3.res_code
             left join t_zz_lithium_battery lithium on lithium.res_code = a3.res_code
             left join t_zz_switch_power swtitch on swtitch.res_code = a3.res_code
    where 
        device.device_type in (select device_type from hidden_danger_code_dict where rule_type = 1) and a3.lifecycle_status != '退网'







--------------------------------------------------------------------------------------------------

测试环境

curl --location --request POST 'localhost:8486/v1/hiddenDanger/rule/testRule?namespace=alauda' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ruleId": 47,
    "deviceDataList": [
        {
            "siteName": "百色测试数据县古障2",
            "deviceId": "00771006000002944984",
            "deviceCode": "150100000000001",
            "deviceName": "科龙柜式空调1",
            "deviceProperty": "",
            "signalId": "017012",
            "signalName": "回风温度设定",
            "signalNum": 0,
            "value": 40.169,
            "date": "2025-10-23 13:59:00"
        }
    ]
}'