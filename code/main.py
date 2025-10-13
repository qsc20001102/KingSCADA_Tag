import os
import tkinter as tk
from ui_main import MainUI
from logger_config import setup_logger

if __name__ == "__main__":
    setup_logger()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(base_dir)   # 上一级目录 

    root = tk.Tk()
    app = MainUI(root, base_dir)
    root.mainloop()
