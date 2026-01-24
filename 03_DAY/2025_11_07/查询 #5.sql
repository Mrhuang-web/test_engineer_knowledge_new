SELECT * FROM t_liquid_cooling_config;
SELECT * FROM t_liquid_cooling_primary_side_config;


SELECT * FROM m_site where siteid IN ('2028','2029','2030');
SELECT * FROM m_room where siteid IN ('2028','2029','2030');
SELECT * FROM m_device WHERE siteid IN ('2028','2029','2030');
SELECT * FROM m_device WHERE roomid IN ('202804');
SELECT * FROM m_signal where deviceid IN ('60291');
SELECT * FROM m_device WHERE roomid IN ('202805');
SELECT * FROM m_signal where deviceid IN ('60344');
SELECT * FROM m_signal WHERE signalid = '013405' AND siteid = 2028

60121
SELECT * FROM m_device WHERE deviceid IN ('60121');
SELECT * FROM m_device WHERE roomid IN ('202806');
SELECT * FROM m_signal where deviceid IN ('60397');


SELECT * FROM m_device WHERE roomid IN ('202806');
SELECT * FROM m_signal where deviceid IN ('60419');


SELECT * FROM m_signal where deviceid IN ('60366');
SELECT * FROM m_signal where signalid IN ('013351') AND siteid = '2028'; 
SELECT * FROM m_device where deviceid IN ('60101');


SELECT *
FROM d_signalh
WHERE id BETWEEN 1110924971 AND 1115947031 AND siteid IN (2028,2029,2030)
AND signaldesc IS NOT NULL 
LIMIT 4000

53547
SELECT * FROM m_device WHERE deviceid = '53547'

SELECT MAX(id) FROM d_signalh LIMIT 2
SELECT id FROM d_signalh GROUP BY id desc LIMIT 10

precint 找dim_xxx  找到mpp里面机房信息  -- 在找到devcie_spatixxx