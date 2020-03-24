import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class View(tk.Tk):
    """Applications root window"""
    
    def __init__(self, controller=None, account=None, *configs):
        """Code goes here"""
        tk.Tk.__init__(self, *configs)
        
        self.controller = controller
        
        self.bankAccount = account
        
        #Below is code for the motherFrame
        self.motherFrame = tk.Frame(self)
        self.motherFrame.grid(row=0, column=0)
        #Need to add all frame classes for each feature into motherFrame

        #Menu not working for some reason, probably due to stacking it on motherFrame
        
        menu = tk.Menu(self.motherFrame)
        self.config(menu=menu)

        file = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File: ', menu=file)
        #file.add_cascade(label='?')
        #Not sure what to add under File: menu

        helpTab = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Help: ', menu=helpTab)
        helpTab.add_command(label='About: ', command=lambda: messagebox.askokcancel("About: ", "Budget Buddy allows you to input your"/
                                                                                    " income and then budgets your money based on expenses"/
                                                                                    " and how much you want to save by the end of a given"/
                                                                                    " timeframe."))
        helpTab.add_command(label='Instructions: ', command=lambda: messagebox.askokcancel("Instructions: ", "Please input the period per"/
                                                                                    " expense you would like to budget yourself. Then add"/
                                                                                    " your expense, frequency of how often you pay for said"/
                                                                                    " expense, then with how much you would like to have saved"/
                                                                                    " by the end of the desired timeframe. Lastly, examine your"/
                                                                                    " visual representation of how much you would have to spend"/
                                                                                    " based on your desired denomination. You are able to save"/
                                                                                    " your budget plan as well as open a new one."))
        

class currentAndGoalBalance(tk.Frame):
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.currentBalanceData = tk.IntVar()
        self.goalBalanceData = tk.IntVar()
        #^[P.S.:]Keep in mind we may have to change these to StringVar's if we want our users to see commas just for better use
        #If we end up implementing this, code for adding decimal point at index[-3] and index[-2:].isdigit(), then add commas /
        #automatically after three numbers inputted
        #In order to convert these to integers, split the commas and add it to one net float value

        '''^What do you guys think?'''

        self.currentBalanceLabel = tk.Label(self, text="Current Balance:")
        self.currentBalanceLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")
        self.currentBalanceEntry = tk.Entry(self, textvariable=self.currentBalanceData)
        self.currentBalanceEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")
        
        self.goalBalanceLabel = tk.Label(self, text="Goal Balance:")
        self.goalBalanceLabel.grid(row=1, column=0, sticky="N"+"E"+"S"+"W")
        self.goalBalanceEntry = tk.Entry(self, textvariable=self.goalBalanceData)
        self.goalBalanceEntry.grid(row=1, column=1, sticky="N"+"E"+"S"+"W")
        
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

class addExpense(tk.Frame):
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.addExpenseButton = Button(master, bg="white", fg="green", text="ADD Expense")
        #^include after text, [command=self.addExpenseFrame]
        #REFERENCE THIS FOR LATER
        self.addExpenseButton.grid(row=0, column=0, columnspan=2, sticky="N"+"E"+"S"+"W")

class Income(tk.Frame): 
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)
        
        self.nameIncomeLabel = tk.Label(self, text="Name of Income")
        self.amountIncomeLabel = tk.Label(self, text="Amount for Income")
        self.timeframeIncomeLabel = tk.Label(self, text="Timeframe of Income")
        self.frequencyIncomeLabel = tk.Label(self, text="Frequency for Income")
        
        self.nameIncomeData = tk.StringVar()
        self.amountIncomeData = tk.IntVar()
        self.timeframeIncomeData = tk.StringVar()
        self.frequencyIncomeData = tk.IntVar()        
        
        self.nameIncomeEntry = tk.Entry(self, textvariable=self.nameIncomeData)
        self.amountIncomeEntry = tk.Entry(self, textvariable=self.amountIncomeData)
        self.timeframeIncomeEntry = tk.OptionMenu(self, self.timeframeIncomeData, "Daily", "Weekly", "Monthly", "Yearly")
        self.frequencyIncomeEntry = tk.Entry(self, textvariable=self.frequencyIncomeData)
        
        self.nameIncomeLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")
        self.nameIncomeEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")
        
        self.amountIncomeLabel.grid(row=0, column=2, sticky="N"+"E"+"S"+"W")
        self.amountIncomeEntry.grid(row=0, column=3, sticky="N"+"E"+"S"+"W")
        
        self.timeframeIncomeLabel.grid(row=0, column=4, sticky="N"+"E"+"S"+"W")
        self.timeframeIncomeEntry.grid(row=0, column=5, sticky="N"+"E"+"S"+"W")
        
        self.frequencyIncomeLabel.grid(row=0, column=6, sticky="N"+"E"+"S"+"W")
        self.frequencyIncomeEntry.grid(row=0, column=7, sticky="N"+"E"+"S"+"W")

class addIncome(tk.Frame):
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.addIncomeButton = Button(master, bg="white", fg="green", text="ADD Income")
        #^include after text, [command=self.addIncomeFrame]
        #REFERENCE THIS FOR LATER
        self.addIncomeButton.grid(row=0, column=0, columnspan=2, sticky="N"+"E"+"S"+"W")

class infoGraph(tk.Frame):
    def __init__(self, parent=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        #[Code here] for mathlib and pandas interaction for graph to appear
        #May need to make an additional frame for displaying the graph, unsure at this current time
