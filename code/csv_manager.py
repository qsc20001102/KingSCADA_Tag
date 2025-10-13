import csv
import os
import logging

logger = logging.getLogger(__name__)

class CSVManager:
    """
    负责 CSV 文件的读取、数据存储、拼接和输出
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.csv_data = []

    def load_csv(self, filepath):
        """自动识别编码读取 CSV 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.csv_data = list(reader)
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='gbk') as f:
                reader = csv.DictReader(f)
                self.csv_data = list(reader)

        if not self.csv_data:
            logger.warning(f"CSV 文件为空或格式错误：{filepath}")
        else:
            logger.info(f"成功加载 CSV：{filepath}，共 {len(self.csv_data)} 行")
        return self.csv_data

    def generate_output(self, template_data, user_inputs):
        """
        根据模板和 CSV 数据拼接生成新的 CSV 文件
        user_inputs 包含：start_id, ip, device_name, group_name, protocol, db_num
        """
        output_path = os.path.join(self.base_dir, 'output', 'generated_tags.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        headers = ["TagName", "Description", "Address", "Type", "Access",
                   "StartID", "IP", "DeviceName", "GroupName", "Protocol", "DB"]

        rows = []
        for device_row in self.csv_data:
            code = device_row['设备代号']
            desc = device_row['设备描述']
            base_offset = float(device_row['起始偏移'])

            for tpl in template_data:
                tag_name = f"{code}{tpl['name']}"
                tag_desc = f"{desc}{tpl['desc']}"
                tag_address = f"DB{user_inputs['db_num']}.{base_offset + float(tpl['address']):.1f}"

                row = [
                    tag_name,
                    tag_desc,
                    tag_address,
                    tpl['type'],
                    tpl['access'],
                    user_inputs['start_id'],
                    user_inputs['ip'],
                    user_inputs['device_name'],
                    user_inputs['group_name'],
                    user_inputs['protocol'],
                    user_inputs['db_num']
                ]
                rows.append(row)

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        logger.info(f"成功生成点表文件：{output_path}（共 {len(rows)} 行）")
        return output_path
