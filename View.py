import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
    """Applications root window"""
    
    def __init__(self, *args, **kwargs):
        """Code goes here"""
        super().__init__(*args, **kwargs)