# 照片相关数据存储

import json
import os

class FaceData:
    """照片数据管理类"""
    
    # 存储配置
    STORAGE_TYPE = 'file'  # 当前存储类型：file，预留：database, cache
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'faces.json')
    # 存储容量限制（字节），20MB=20*1024*1024=20971520，可手动调整
    STORAGE_LIMIT = 20 * 1024 * 1024
    
    def __init__(self):
        # 初始化照片数据列表
        self._faces = []
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从存储中加载数据"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    with open(self.STORAGE_PATH, 'r', encoding='utf-8') as f:
                        self._faces = json.load(f)
            except Exception as e:
                print(f"加载照片数据失败: {e}")
        # 预留数据库或缓存加载逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库加载逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存加载逻辑
            pass
    
    def save_data(self):
        """将数据保存到存储中"""
        if self.STORAGE_TYPE == 'file':
            try:
                with open(self.STORAGE_PATH, 'w', encoding='utf-8') as f:
                    json.dump(self._faces, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存照片数据失败: {e}")
        # 预留数据库或缓存保存逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库保存逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存保存逻辑
            pass
    
    def check_storage_usage(self):
        """检查存储使用情况"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    file_size = os.path.getsize(self.STORAGE_PATH)
                    return file_size
            except Exception as e:
                print(f"检查存储使用情况失败: {e}")
        return 0
    
    def add_face(self, face):
        """添加照片"""
        # 先添加照片到临时列表计算新大小
        temp_faces = self._faces.copy()
        temp_faces.append(face)
        
        # 计算添加新照片后的估计大小
        import json
        temp_data = json.dumps(temp_faces)
        estimated_size = len(temp_data) * 2  # 预估 JSON 存储大小（考虑到缩进等）
        
        # 检查实际当前大小
        current_size = self.check_storage_usage()
        
        # 只有当实际大小 + 预估新照片大小超过限制时才拒绝
        if current_size + estimated_size > self.STORAGE_LIMIT:
            return False
        
        # 实际添加照片
        self._faces.append(face)
        self.save_data()
        return True
    
    def get_face(self, face_id):
        """根据ID获取照片"""
        # 重新加载数据，确保获取最新内容（解决手动编辑文件后数据不同步问题）
        self.load_data()
        for face in self._faces:
            if face['faceId'] == face_id:
                return face
        return None
    
    def get_faces_by_person(self, person_id):
        """根据人员ID获取所有照片"""
        # 重新加载数据，确保获取最新内容（解决手动编辑文件后数据不同步问题）
        self.load_data()
        return [face for face in self._faces if face['personId'] == person_id]
    
    def delete_face(self, face_id):
        """删除照片"""
        original_length = len(self._faces)
        self._faces = [f for f in self._faces if f['faceId'] != face_id]
        if len(self._faces) < original_length:
            self.save_data()
            return True
        return False
    
    def delete_faces_by_person(self, person_id):
        """删除指定人员的所有照片"""
        original_length = len(self._faces)
        self._faces = [f for f in self._faces if f['personId'] != person_id]
        if len(self._faces) < original_length:
            self.save_data()
            return True
        return False
    
    def update_face(self, updated_face):
        """更新照片信息"""
        for i, face in enumerate(self._faces):
            if face['faceId'] == updated_face['faceId']:
                self._faces[i] = updated_face
                self.save_data()
                return True
        return False

# 创建照片数据实例
face_data = FaceData()