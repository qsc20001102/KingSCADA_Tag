import os
import tkinter as tk
from core.ui_main import MainUI
from core.logger_config import setup_logger

if __name__ == "__main__":
    setup_logger()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    root = tk.Tk()
    app = MainUI(root, base_dir)
    root.mainloop()
