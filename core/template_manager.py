import os
import json
import logging

logger = logging.getLogger(__name__)

class TemplateManager:
    """
    负责管理设备类型、模板文件加载和数据存储
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.template_data = []

    def get_device_types(self):
        """获取 tag_config 目录下的设备类型列表"""
        tag_config_dir = os.path.join(self.base_dir, 'tag_config')
        if not os.path.exists(tag_config_dir):
            os.makedirs(tag_config_dir)
            logger.warning(f"tag_config 目录不存在，已自动创建：{tag_config_dir}")
        return [d for d in os.listdir(tag_config_dir)
                if os.path.isdir(os.path.join(tag_config_dir, d))]

    def get_templates_by_device(self, device_type):
        """列出某个设备类型下的所有 json 模板"""
        device_path = os.path.join(self.base_dir, 'tag_config', device_type)
        if not os.path.exists(device_path):
            logger.error(f"设备目录不存在：{device_path}")
            return []
        return [f for f in os.listdir(device_path) if f.endswith('.json')]

    def load_template(self, device_type, filename):
        """加载选中的模板 JSON 文件"""
        file_path = os.path.join(self.base_dir, 'tag_config', device_type, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.template_data = json.load(f)
            logger.info(f"已加载模板文件：{file_path}")
        except Exception as e:
            logger.exception(f"加载模板文件失败：{file_path}")
            self.template_data = []
        return self.template_data
