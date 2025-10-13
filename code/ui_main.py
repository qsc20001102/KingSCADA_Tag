import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from template_manager import TemplateManager
from csv_manager import CSVManager
import logging

logger = logging.getLogger(__name__)

class MainUI:
    def __init__(self, root, base_dir):
        self.root = root
        self.root.title("KingSCADA 点表生成工具")
        self.root.geometry("1000x750")

        self.base_dir = base_dir
        self.template_manager = TemplateManager(base_dir)
        self.csv_manager = CSVManager(base_dir)

        self.template_data = []
        self.csv_data = []

        self.build_ui()

    def build_ui(self):
        self.create_template_section()
        self.create_input_section()
        self.create_csv_section()
        self.create_generate_section()

    # ---------------- 模板区 ----------------
    def create_template_section(self):
        frame = ttk.LabelFrame(self.root, text="配置文件选择", padding=10)
        frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame, text="设备类型：").grid(row=0, column=0, sticky='w')
        self.device_var = tk.StringVar()
        self.device_cb = ttk.Combobox(frame, textvariable=self.device_var, state='readonly')
        self.device_cb['values'] = self.template_manager.get_device_types()
        self.device_cb.bind('<<ComboboxSelected>>', self.on_device_selected)
        self.device_cb.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="模板文件：").grid(row=0, column=2, sticky='w')
        self.template_var = tk.StringVar()
        self.template_cb = ttk.Combobox(frame, textvariable=self.template_var, state='readonly')
        self.template_cb.bind('<<ComboboxSelected>>', self.on_template_selected)
        self.template_cb.grid(row=0, column=3, padx=5)

        self.template_table = ttk.Treeview(frame, columns=("name","desc","type","access","address"), show="headings", height=5)
        for col in ("name","desc","type","access","address"):
            self.template_table.heading(col, text=col)
        self.template_table.grid(row=1, column=0, columnspan=4, sticky='nsew', pady=5)

    def on_device_selected(self, event=None):
        device = self.device_var.get()
        self.template_cb['values'] = self.template_manager.get_templates_by_device(device)

    def on_template_selected(self, event=None):
        device = self.device_var.get()
        template = self.template_var.get()
        self.template_data = self.template_manager.load_template(device, template)
        self.refresh_template_table()

    def refresh_template_table(self):
        for row in self.template_table.get_children():
            self.template_table.delete(row)
        for item in self.template_data:
            self.template_table.insert('', 'end', values=(item['name'], item['desc'], item['type'], item['access'], item['address']))

    # ---------------- 参数区 ----------------
    def create_input_section(self):
        frame = ttk.LabelFrame(self.root, text="参数输入", padding=10)
        frame.pack(fill='x', padx=10, pady=5)

        self.start_id = self._add_input(frame, "起始ID", 0)
        self.ip = self._add_input(frame, "设备IP", 1)
        self.dev_name = self._add_input(frame, "设备名称", 2)
        self.group_name = self._add_input(frame, "分组名称", 3)

        ttk.Label(frame, text="协议类型：").grid(row=1, column=0, sticky='w')
        self.protocol_var = tk.StringVar()
        self.protocol_cb = ttk.Combobox(frame, textvariable=self.protocol_var, state='readonly')
        self.protocol_cb['values'] = ["S7-300", "S7-1200", "S7-1500"]
        self.protocol_cb.grid(row=1, column=1, padx=5, pady=5)

        self.db_num = self._add_input(frame, "DB块号", 1, col=2)

    def _add_input(self, parent, label, row, col=0):
        ttk.Label(parent, text=label+"：").grid(row=row, column=col*2, sticky='w')
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var, width=20)
        entry.grid(row=row, column=col*2+1, padx=5, pady=5)
        return var

    # ---------------- CSV区 ----------------
    def create_csv_section(self):
        frame = ttk.LabelFrame(self.root, text="CSV 数据导入", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        btn = ttk.Button(frame, text="选择CSV文件", command=self.load_csv_file)
        btn.pack(anchor='w')

        self.csv_table = ttk.Treeview(frame, columns=("code","desc","offset"), show="headings")
        for col in ("code","desc","offset"):
            self.csv_table.heading(col, text=col)
        self.csv_table.pack(fill='both', expand=True, pady=5)

    def load_csv_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        self.csv_data = self.csv_manager.load_csv(filepath)
        self.refresh_csv_table()

    def refresh_csv_table(self):
        for row in self.csv_table.get_children():
            self.csv_table.delete(row)
        for row in self.csv_data:
            self.csv_table.insert('', 'end', values=(row['设备代号'], row['设备描述'], row['起始偏移']))

    # ---------------- 生成区 ----------------
    def create_generate_section(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill='x', padx=10, pady=5)

        btn = ttk.Button(frame, text="生成点表文件", command=self.generate_csv)
        btn.pack(anchor='e')

    def generate_csv(self):
        if not self.template_data or not self.csv_data:
            messagebox.showwarning("警告", "请先加载模板和CSV数据！")
            return

        inputs = {
            "start_id": self.start_id.get(),
            "ip": self.ip.get(),
            "device_name": self.dev_name.get(),
            "group_name": self.group_name.get(),
            "protocol": self.protocol_var.get(),
            "db_num": self.db_num.get()
        }

        output_path = self.csv_manager.generate_output(self.template_data, inputs)
        messagebox.showinfo("生成成功", f"点表已生成：\n{output_path}")
