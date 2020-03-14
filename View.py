import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
    """Applications root window"""
    
    def __init__(self, *args, **kwargs):
        """Code goes here"""
        super().__init__(*args, **kwargs)
        
        self.exspense1 = Exspense(self)
        self.exspense1.grid(row=0, column=0)

class Exspense(tk.Frame): 
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)
        
        self.nameLabel = tk.Label(self, text="Name")
        self.amountLabel = tk.Label(self, text="Amount")
        self.timeframeLabel = tk.Label(self, text="Timeframe")
        self.frequencyLabel = tk.Label(self, text="Frequency")
        
        self.nameData = tk.StringVar()
        self.amountData = tk.IntVar()
        self.timeframeData = tk.StringVar()
        self.frequencyData = tk.IntVar()        
        
        self.nameEntry = tk.Entry(self, textvariable=self.nameData)
        self.amountEntry = tk.Entry(self, textvariable=self.amountData)
        self.timeframeEntry = tk.OptionMenu(self, self.timeframeData, "Daily", "Weekly", "Monthly", "Yearly")
        self.frequencyEntry = tk.Entry(self, textvariable=self.frequencyData)
        
        self.nameLabel.grid(row=0, column=0)
        self.nameEntry.grid(row=0, column=1)
        
        self.amountLabel.grid(row=0, column=2)
        self.amountEntry.grid(row=0, column=3)
        
        self.timeframeLabel.grid(row=0, column=4)
        self.timeframeEntry.grid(row=0, column=5)
        
        self.frequencyLabel.grid(row=0, column=6)
        self.frequencyEntry.grid(row=0, column=7)
        
        
        