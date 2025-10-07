"""
main.py - Application principale LightControl Pro
"""
import tkinter as tk
from light_control import LightControlApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LightControlApp(root)
    root.mainloop()