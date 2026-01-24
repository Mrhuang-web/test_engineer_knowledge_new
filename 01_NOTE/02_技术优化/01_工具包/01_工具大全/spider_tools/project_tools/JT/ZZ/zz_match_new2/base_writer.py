import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch, helpers

from spider_tools.project_tools.JT.ZZ.zz_match_new2.databuilder import DataBuilder
from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig


# ==================== 基础写入器 ====================
class BaseWriter:
    """统一的基础写入器 - 合并原始BaseESWriter功能"""
    # 22 类索引的全部字段（去重后）
    ALL_FIELDS = set(
        fld
        for dev_fields in DataBuilder.DEVICE_FIELDS.values()
        for fld in dev_fields
    )

    def __init__(self, index_type: str, **kwargs):
        self.index_type = index_type
        self.es = Elasticsearch(ESConfig.ES_URL)
        self.doc_type = "point_history_data"
        # 保留所有原始业务参数
        self._load_business_params(kwargs)

        # 生成索引名
        self.index_name = self._generate_index_name()

        print(f"[{self.__class__.__name__}] 初始化完成")
        print(f"  - 索引类型: {self.index_type}")
        print(f"  - 索引名称: {self.index_name}")

    def _load_business_params(self, kwargs: Dict[str, Any]):
        """加载业务参数 - 保留原始全部参数"""

        # 站点相关
        self.site_type = kwargs.get('site_type', '核心站点')
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.batch_num = kwargs.get('batch_num', f"BATCH_{datetime.now().strftime('%Y%m%d')}")
        self.related_dc = kwargs.get('related_dc', "")
        self.site_zh_label = kwargs.get('site_zh_label', f"test_{datetime.now().strftime('%Y%m%d')}")
        self.site_pro_zh_label = kwargs.get('site_pro_zh_label', f"ROOM_{random.randint(1000, 9999)}")
        self.power_monitoring_site_name = kwargs.get('power_monitoring_site_name', f"site_{random.randint(1000, 9999)}")

        # 地域相关
        self.county_id = kwargs.get('county_id', '000000')
        self.province_id = kwargs.get('province_id', '520000')
        self.city_id = kwargs.get('city_id', '520400')

        # 时间相关
        self.date = kwargs.get('date', datetime.now().strftime('%Y%m%d'))

        # ID相关
        self.site_int_id = kwargs.get('site_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_int_id = kwargs.get('room_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.site_res_code = kwargs.get('site_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_res_code = kwargs.get('room_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.site_pro_res_code = kwargs.get('site_pro_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_pro_res_code = kwargs.get('room_pro_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))

        # 机房相关
        self.room_zh_label = kwargs.get('room_zh_label', f"ROOM_{random.randint(1000, 9999)}")
        self.room_dh_name = kwargs.get('room_dh_name', f"DH_{random.randint(1000, 9999)}")
        self.room_zg_name = kwargs.get('room_zg_name', f"ZG_{random.randint(1000, 9999)}")
        self.room_pro_zh_label = kwargs.get('room_pro_zh_label', f"ROOM_{random.randint(1000, 9999)}")

        # 设备相关
        self.power_device_id = kwargs.get('power_device_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_res_code = kwargs.get('device_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_zh_label = kwargs.get('device_zh_label', f"device_{random.randint(1000, 9999)}")

        # 扩充 - 其他业务参数可继续添加（汇聚机房）
        self.cutin_date = kwargs.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        self.mains_nature = kwargs.get('mains_nature', random.choice(['市电转供', '市电直供', '其他']))
        self.power_site_level = kwargs.get('power_site_level',
                                           random.choice(['通信机楼', '数据中心', '传输节点', '通信基站']))
        self.power_room_type = kwargs.get('power_room_type',
                                          random.choice(['传输机房', '交换机房', '数据机房', '汇聚机房']))
        self.power_supply_mode = kwargs.get('power_supply_mode',
                                            random.choice(['双电源双回路供电', '单电源双回路供电', '其他']))
        self.site_type = kwargs.get('site_type', random.choice(
            ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']))
        self.power_related_site_name = kwargs.get('power_related_site_name', f"site_{random.randint(1000, 9999)}")

        # 扩展

        # 兜底 - 其他参数
        for fld in self.ALL_FIELDS:
            if fld not in kwargs:
                continue
            setattr(self, fld, kwargs[fld])

    def _generate_index_name(self) -> str:
        """生成索引名 - 保留原始复杂逻辑"""
        prefix = ESConfig.INDEX_PREFIX_MAP.get(self.index_type)
        if not prefix:
            raise ValueError(f"未知的索引类型: {self.index_type}")

        # 根据业务规则生成后缀
        for suffix_format, types in ESConfig.INDEX_SUFFIX_RULES.items():
            if self.index_type in types:
                if suffix_format == 'YYYYMMm':
                    suffix = self._get_suffix_from_batch(6) + 'm'
                elif suffix_format == 'YYYYy':
                    suffix = self._get_suffix_from_batch(4) + 'y'
                elif suffix_format == 'YYYYMMDDd':
                    suffix = self._get_suffix_from_date() + 'd'
                else:
                    suffix = self.date
                break
        else:
            suffix = self.date

        return f"{prefix}_{suffix}"

    def _get_suffix_from_batch(self, length: int) -> str:
        """从batch_num提取后缀"""
        if self.batch_num and len(self.batch_num) >= length:
            return self.batch_num[:length]
        return datetime.now().strftime('%Y%m' if length == 6 else '%Y')

    def _get_suffix_from_date(self) -> str:
        """从date提取后缀"""
        if self.batch_num and len(self.batch_num) == 8:
            return self.batch_num
        return self.date

    def create_index(self, mapping: Optional[Dict] = None, force_create: bool = False):
        """创建索引 - 保留原始安全逻辑"""
        exists = self.es.indices.exists(index=self.index_name)

        if exists and not force_create:
            print(f"索引已存在，将追加数据: {self.index_name}")
            self._show_index_stats()
            return

        if exists and force_create:
            print(f"强制删除并重建索引: {self.index_name}")
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])

        print(f"创建索引: {self.index_name}")
        self.es.indices.create(index=self.index_name, ignore=[400])

        # 设置配置和mapping
        self._apply_settings_and_mapping(mapping)
        print(f"索引创建成功")

    def _apply_settings_and_mapping(self, mapping: Optional[Dict]):
        """应用设置和mapping"""
        self.es.indices.put_settings(
            index=self.index_name,
            body=ESConfig.INDEX_SETTINGS
        )

        if mapping:
            self.es.indices.put_mapping(
                index=self.index_name,
                doc_type=self.doc_type,
                body={self.doc_type: mapping}
            )
            print(f"  - Mapping已创建")

    def _show_index_stats(self):
        """显示索引统计"""
        try:
            stats = self.es.count(index=self.index_name)
            print(f"  - 当前文档数: {stats.get('count', 0):,} 条")
        except:
            pass
        print(f"提示：如需强制重建，请设置 force_create=True")

    def bulk_write(self, data_list: List[Dict]):
        """批量写入 - 保留原始反馈逻辑"""
        if not data_list:
            print("  - 无数据需要写入")
            return

        actions = [
            {"_index": self.index_name, "_type": self.doc_type, "_source": data}
            for data in data_list
        ]

        try:
            success, failed = helpers.bulk(self.es, actions, stats_only=True)
            print(f"写入成功: {success}条, 失败: {failed}条")

            # 显示总数
            self._show_index_stats()
            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"❌ 批量写入失败: {e}")

    # ====== 新增：统一的 write 方法 ======
    def write(self, count: int = 100, force_create: bool = False):
        """
        完整流程：生成数据并写入 - 原为BaseESWriter的核心方法
        :param count: 生成数据条数
        :param force_create: 是否强制重建索引（危险操作）
        """
        print(f"\n[{self.index_type}] 开始写入流程...")
        print(f"  - 准备生成 {count} 条数据")

        # 检查索引存在性并创建（安全模式）
        self.create_index(force_create=force_create)

        # 生成数据（子类必须实现 generate_mock_data）
        print(f"  - 生成模拟数据中...")
        data_list = self.generate_mock_data(count)
        print(f"  - 数据生成完成")

        # 写入ES
        self.bulk_write(data_list)

        print(f"[{self.index_type}] 写入流程完成\n")

    def generate_mock_data(self, count: int) -> List[Dict]:
        """
        生成模拟数据 - 抽象方法，子类必须实现
        这是原始 BaseESWriter 的要求，必须保留
        """
        raise NotImplementedError(f"子类 {self.__class__.__name__} 必须实现 generate_mock_data 方法")
