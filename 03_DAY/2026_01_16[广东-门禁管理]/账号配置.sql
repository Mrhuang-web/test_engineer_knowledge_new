select if(count(*) > 0, true, false) checkFlag from entrance_card;
SELECT * from entrance_card;

select uuid from entrance_user where code = ? and is_sys_sync = 1 and isdel = 0

insert into entrance_card(`card_id`, `belong_user`, `current_user`, `create_user`, `create_time`, `isdel`) 
values ( ?, ?, ?, ?, now(), 0 )

select uuid from entrance_user


insert into entrance_card (id,card_id, belong_user, current_user,create_user,create_time,isdel)
            values ('218', '1212121212', '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f', '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f', '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f', '2024-07-09 15:59:55', 0)

select * from entrance_user;
SELECT * from entrance_card;
SELECT * FROM entrance_card_auth;
SELECT * FROM access_control_device GROUP BY access_mode;

SELECT * FROM t_cfg_dict WHERE col_name = 'access_mode';

SELECT * FROM t_cfg_device
WHERE device_id IN (SELECT device_id FROM access_control_device );

9f4f460f-d6f0-45fd-97e3-e2a390eed5fc

2c729fef-53d8-4c5d-b8b3-e42e811cfc1f
fd08df32-495c-4bc1-9359-ee6c8b18caaa

insert into entrance_card_auth(`card_id`, `device_id`, `user_id`, `password`, `expiration`, `isdel`, `current_user`, `create_user`, `create_time`, `update_time`) 
VALUES('ABC120', '9f4f460f-d6f0-45fd-97e3-e2a390eed5fc', null, 
NULL , '2026-01-17', 0, '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f', 'fd08df32-495c-4bc1-9359-ee6c8b18caaa', now(), NOW())



SELECT * FROM 



select *
from entrance_card ec left join entrance_user eu on ec.current_user = eu.uuid and eu.isdel = 0 where ec.card_id = '1212121212' and ec.isdel = 0


SELECT *
FROM entrance_card WHERE belong_user = '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f' AND card_id = '1212121212';

SELECT *
FROM entrance_user WHERE uuid = '2c729fef-53d8-4c5d-b8b3-e42e811cfc1f';



select * from access_control_device where room_id = '01-01-17-02-05-01' and door_name != ''
SELECT * FROM entrance_card;





select * from access_control_device where room_id = '01-01-17-02-05-01' and door_name != '';
UPDATE access_control_device SET ip_address = '10.12.5.142' where room_id = '01-01-17-02-05-01' and door_name != '';
select * from t_cfg_fsu where room_id = '01-01-17-02-05-01' and door_name != '';


SELECT * FROM entrance_card_auth;