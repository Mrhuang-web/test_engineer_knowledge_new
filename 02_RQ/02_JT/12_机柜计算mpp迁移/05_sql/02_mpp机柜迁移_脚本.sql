
-- 机柜管理，添加字段
ALTER TABLE `energy_cabinet_column`
ADD COLUMN `sort_order` int COMMENT '列顺序号，0-9999的正整数',
ADD COLUMN `channel_name` varchar(64) DEFAULT NULL COMMENT '所属封闭通道，同一机房下，相同通道名称的机柜列，自动按通道组合',
ADD COLUMN `channel_type` tinyint(1) DEFAULT NULL COMMENT '封闭通道类型，1-冷，2-热';



ALTER TABLE `energy_cabinet`
ADD COLUMN `sort_order` int COMMENT '列顺序号，0-9999的正整数',
ADD COLUMN `cabinet_type` char(1) DEFAULT '1' COMMENT '机柜类别，枚举：1-机柜、2-列间空调、3-列头柜、4-立柱';



ALTER TABLE `energy_cabinet_attribute_config`
MODIFY COLUMN `config_type` int COMMENT '配置类型1：供电类型1;2：供电类型2;3：供电类型3;4：供电类型4; 5：机柜前;6：机柜后;',
MODIFY COLUMN `type` int COMMENT '供电类型：1:电压  2：电流  3：功率  4：电能；机柜前后：1.上温度   2.中温度  3.下温度 ；4.上湿度   5.中湿度  6.下湿度';

-- 机柜类别 枚举：1-机柜、2-列间空调、3-列头柜、4-立柱。默认为 1-机柜
INSERT INTO `t_cfg_dict`(`dict_id`, `dict_code`, `col_name`, `dict_note`, `up_dict`)
SELECT max(dict_id)+1, '1', 'cabinetType', '机柜', 0 FROM t_cfg_dict;

INSERT INTO `t_cfg_dict`(`dict_id`, `dict_code`, `col_name`, `dict_note`, `up_dict`)
SELECT max(dict_id)+1, '2', 'cabinetType', '列间空调', 0 FROM t_cfg_dict;

INSERT INTO `t_cfg_dict`(`dict_id`, `dict_code`, `col_name`, `dict_note`, `up_dict`)
SELECT max(dict_id)+1, '3', 'cabinetType', '列头柜', 0 FROM t_cfg_dict;

INSERT INTO `t_cfg_dict`(`dict_id`, `dict_code`, `col_name`, `dict_note`, `up_dict`)
SELECT max(dict_id)+1, '4', 'cabinetType', '立柱', 0 FROM t_cfg_dict;
