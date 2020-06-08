import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class View(tk.Tk):
    """Applications root window"""

    def __init__(self, controller=None, account=None, *config):
        tk.Tk.__init__(self, *config)

        self.title("Budget Buddy")

        self.controller = controller

        self.account = account

        #Below is code for the motherFrame (application's skeleton)
        self.motherFrame = tk.Frame(self)
        self.motherFrame.grid(row=0, column=0, columnspan=7)

        #GUI for graph timeframe
        self.timeframeLabel = tk.Label(self, text="Select Time Interval:")
        self.timeframe = tk.StringVar()
        self.timeframe.set("Day")
        self.timeframeMenu = tk.OptionMenu(self, self.timeframe, "Day", "Week", "Month", "Year")
        self.timeframeLabel.grid(row=2, column=0, sticky="NSEW")
        self.timeframeMenu.grid(row=2, column=1, sticky="NSEW")

        #Repeat section coded to account for multiple days, weeks, months, and years
        self.repeatsLabel = tk.Label(self, text="Repeat Interval:")
        self.repeats = tk.IntVar()
        self.repeats.set(1)
        self.repeatsBTN = tk.Entry(self, textvariable=self.repeats)
        self.repeatsLabel.grid(row=2, column=2, sticky="NSEW")
        self.repeatsBTN.grid(row=2, column=3, sticky="NSEW")

        #Code for graphing button in the GUI
        self.graphBTN = tk.Button(self, text="Graph", padx=25, pady=15, command=self.graph)
        self.graphBTN.grid(row=3, column=0, columnspan=2, sticky="NSEW")

        #GUI for output values
        self.initialBalanceOutput = tk.IntVar()
        self.finalBalanceOutput = tk.IntVar()
        self.netOutput = tk.IntVar()
        self.goalOutput = tk.IntVar()

        #Next several labels and values included to show user input as well as user output
        self.initialBalanceLabel = tk.Label(self, text="Initial Balance:")
        self.initialBalanceValue = tk.Label(self, textvariable=self.initialBalanceOutput)
        self.initialBalanceLabel.grid(row=4, column=0, sticky="NSEW")
        self.initialBalanceValue.grid(row=4, column=1, sticky="NSEW")

        self.finalBalanceLabel = tk.Label(self, text="Final Balance:")
        self.finalBalanceValue = tk.Label(self, textvariable=self.finalBalanceOutput)
        self.finalBalanceLabel.grid(row=4, column=2, sticky="NSEW")
        self.finalBalanceValue.grid(row=4, column=3, sticky="NSEW")

        self.netOutputLabel = tk.Label(self, text="Net Gain/Loss:")
        self.netOutputValue = tk.Label(self, textvariable=self.netOutput)
        self.netOutputLabel.grid(row=4, column=4, sticky="NSEW")
        self.netOutputValue.grid(row=4, column=5, sticky="NSEW")

        self.goalOutputLabel = tk.Label(self, text="Goal Difference:")
        self.goalOutputValue = tk.Label(self, textvariable=self.goalOutput)
        self.goalOutputLabel.grid(row=4, column=6, sticky="NSEW")
        self.goalOutputValue.grid(row=4, column=7, sticky="NSEW")

        self.accountBalanceFrame = currentAndGoalBalance(self.motherFrame, self, padx=25, pady=25)
        self.accountBalanceFrame.grid(row=0, column=0, sticky="NSEW")


        #Expenses attributes
        self.expenses = []

        self.expenseLabel = tk.Label(self.motherFrame, text="EXPENSES")
        self.expenseLabel.grid(row=1, column=0)

        self.expenseFrame = ScrollableFrame(self.motherFrame)
        self.expenseFrame.grid(row=2, column=0, sticky="NSEW")

        self.addExpenseBTN = tk.Button(self.motherFrame, text="Add Expense", padx=25, pady=15, command=self.addExpenseFrame)
        self.addExpenseBTN.grid(row=3, column=0, sticky="NSEW")


        #Incomes attributes
        self.incomes = []

        self.incomeLabel = tk.Label(self.motherFrame, text="INCOME")
        self.incomeLabel.grid(row=4, column=0)

        self.incomeFrame = ScrollableFrame(self.motherFrame)
        self.incomeFrame.grid(row=5, column=0, sticky="NSEW")

        self.addIncomeBTN = tk.Button(self.motherFrame, text="Add Income", padx=25, pady=15, command=self.addIncomeFrame)
        self.addIncomeBTN.grid(row=6, column=0, columnspan=2, sticky="NSEW")

        #Menu attributes
        menu = tk.Menu(self.motherFrame)
        self.config(menu=menu)

        file = tk.Menu(menu, tearoff=0)
        file.add_command(label="New Budget", command=self.new)
        file.add_command(label="Save Budget", command=self.save)
        file.add_command(label="Load Budget", command=self.load)

        menu.add_cascade(label='File', menu=file)

        helpTab = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Help', menu=helpTab)
        helpTab.add_command(label='About: ', command=lambda: messagebox.askokcancel("About: ", "Budget Buddy allows you to input your"
                                                                                    " income and then budgets your money based on expenses"
                                                                                    " and how much you want to save by the end of a given"
                                                                                    " timeframe."))
        helpTab.add_command(label='Instructions: ', command=lambda: messagebox.askokcancel("Instructions: ", "Please input the period per"
                                                                                    " expense you would like to budget yourself. Then add"
                                                                                    " your expense, frequency of how often you pay for said"
                                                                                    " expense, then with how much you would like to have saved"
                                                                                    " by the end of the desired timeframe. Lastly, examine your"
                                                                                    " visual representation of how much you would have to spend"
                                                                                    " based on your desired denomination. You are able to save"
                                                                                    " your budget plan as well as open a new one."))
        helpTab.add_command(label='Application Details', command=lambda: messagebox.askokcancel("Application Details:", "Programmed by Jeremy Nguyen, Jose Rivera,"
                                                                                                " Alexander Sigarev, and Ryan Wong originally as a group project"
                                                                                                " for the course CCT211: User Interface Programming, offered at the"
                                                                                                " University of Toronto. During the COVID-19 outbreak, our group found"
                                                                                                " that this application would be immensely helpful to others for staying"
                                                                                                " on top of their finances during the outbreak and anytime afterwards."
                                                                                                " After numerous bugfixes and improvements, Budget Buddy has been updated"
                                                                                                " to the current version you are using."))

    def new(self):
        #This response-if statement combo is used to make sure users want to make a new file. Can be used for loading files
        response = messagebox.askyesno("Making New File", "All unsaved changes will be lost. Create a new budget?")
        if response:
            self.account.clear()
            if self.expenses != []:
                for index in range(0, len(self.expenses)):
                    self.expenses[index].destroy()
                self.expenses.clear()

            if self.incomes != []:
                for index in range(0, len(self.incomes)):
                    self.incomes[index].destroy()
                self.incomes.clear()
        return

    def save(self):
        #View portion of code in Model.py relevant to saving user budget layout. Hardcoded to only save as .csv files to prevent possible errors by the user when saving
        f = filedialog.asksaveasfilename(filetypes=[("Excel spreadsheet", "*.csv")], defaultextension=".csv")
        if f:
            #Calls the save function in controller
            self.controller.save(f)
            messagebox.showinfo("File Save", "Budget saved to " + f)
        return

    def load(self):
        #View portion of code in Model.py relevant to loading user budget layout. Hardcoded to only recognize and load .csv files to add convience for users
        response = messagebox.askyesno("Loading New File", "All unsaved changes will be lost. Load a budget from file?")
        if response:
            f = filedialog.askopenfilename(filetypes=[("Excel spreadsheet", "*.csv")])
            if f:
                #Calls the load function in controller
                self.controller.load(f)

                #Sets the balance info to the account balance entries
                self.accountBalanceFrame.currentBalanceData.set(self.account.balance)
                self.accountBalanceFrame.goalBalanceData.set(self.account.goal)

                #Destroys/Deletes the current income/expense frames in the window
                if self.expenses != []:
                    for index in range(0, len(self.expenses)):
                        self.expenses[index].destroy()


                if self.incomes != []:
                    for index in range(0, len(self.incomes)):
                        self.incomes[index].destroy()

                #Then clears the lists
                self.incomes.clear()
                self.expenses.clear()

                #And finally fills both lists and the window with new income/expense frames
                for index in range(0, len(self.account.expenses)):
                    new = Expense(self.expenseFrame.scrollable_frame, self, pady=25, padx=25)
                    self.expenses.append(new)
                    new.pack(side="top", expand="TRUE", fill="both")

                    self.expenses[index].nameData.set(self.account.expenses[index].name)
                    self.expenses[index].amountData.set(self.account.expenses[index].amount)
                    self.expenses[index].timeframeData.set(self.account.expenses[index].timeframe)
                    self.expenses[index].frequencyData.set(self.account.expenses[index].frequency)


                for index in range(0, len(self.account.incomes)):
                    new = Income(self.incomeFrame.scrollable_frame, self, pady=25, padx=25)
                    self.incomes.append(new)
                    new.pack(side="top", expand="TRUE", fill="both")

                    self.incomes[index].nameData.set(self.account.incomes[index].name)
                    self.incomes[index].amountData.set(self.account.incomes[index].amount)
                    self.incomes[index].timeframeData.set(self.account.incomes[index].timeframe)
                    self.incomes[index].frequencyData.set(self.account.incomes[index].frequency)

                #A dialog showing that the requested file has been loaded
                messagebox.showinfo("File Load", f + " Loaded")
        return

    #Recognizes days/weeks/months/years amount and converting into number of days
    def lengthInDays(self):
        if self.timeframe.get() == "Day":
            return 1 * self.repeats.get()
        elif self.timeframe.get() == "Week":
            return 7 * self.repeats.get()
        elif self.timeframe.get() == "Month":
            return 30 * self.repeats.get()
        elif self.timeframe.get() == "Year":
            return 365 * self.repeats.get()

    #Code for graph output
    def graph(self):
        #Focuses on self
        self.graphBTN.focus_set()

        #Manually updates all the entries
        self.accountBalanceFrame._update()

        for expense in self.expenses:
            expense._update()

        for income in self.incomes:
            income._update()

        #Graph Setup and Output

        self.account.plotBalance = []
        self.account.plotDay = []

        length = self.lengthInDays()
        self.account.graphBalance(length)

        amounts = self.account.getPlotBalance()
        days = self.account.getPlotDay()

        graphWindow = tk.Tk()
        graphWindow.title("Charted Balance")
        chart = infoGraph(graphWindow, amounts, days)
        chart.pack(side="top")

        self.initialBalanceOutput.set(self.account.initial_balance)
        self.finalBalanceOutput.set(self.account.plotBalance[len(self.account.plotBalance) -1])
        self.netOutput.set(self.account.getNetOutput())
        self.goalOutput.set(self.account.getGoalOutput())
        return

    def addExpenseFrame(self):

        #Instantiated a new Expense as new
        new = Expense(self.expenseFrame.scrollable_frame, self, pady=25, padx=25)
        #Adds new to the list of expenses
        self.expenses.append(new)

        #Adds new to the model
        self.account.addExpense([new.nameData.get(), new.amountData.get(), new.timeframeData.get(), new.frequencyData.get()])

        #Grids the expense frame onto the window
        new.pack(side="top", expand="TRUE", fill="both")
        return

    def addIncomeFrame(self):

        #Same process for addExpenseFrame just dealing with income instead now
        new = Income(self.incomeFrame.scrollable_frame, self, pady=25, padx=25)
        self.incomes.append(new)

        self.account.addIncome([new.nameData.get(), new.amountData.get(), new.timeframeData.get(), new.frequencyData.get()])

        new.pack(side="top", expand="TRUE", fill="both")
        return

class currentAndGoalBalance(tk.Frame):
    def __init__(self, parent=None, main=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.rootWin = main

        self.currentBalanceData = tk.IntVar()
        self.goalBalanceData = tk.IntVar()

        self.currentBalanceLabel = tk.Label(self, text="Current Balance:")
        self.currentBalanceLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")

        self.valid = self.register(self._validate)

        self.currentBalanceEntry = tk.Entry(self, textvariable=self.currentBalanceData, validate="all", validatecommand=(self.valid, "%V"))
        self.currentBalanceEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")

        self.goalBalanceLabel = tk.Label(self, text="Goal Balance:")
        self.goalBalanceLabel.grid(row=1, column=0, sticky="N"+"E"+"S"+"W")
        self.goalBalanceEntry = tk.Entry(self, textvariable=self.goalBalanceData, validate="all", validatecommand=(self.valid, "%V"))
        self.goalBalanceEntry.grid(row=1, column=1, sticky="N"+"E"+"S"+"W")

    def _update(self):
        self.rootWin.account.setBalance(self.currentBalanceData.get())
        self.rootWin.account.goal = self.goalBalanceData.get()
        return True

    def _validate(self, event):
        #Ensures validation upon user input
        if event == "focusout":
            self._update()
        return True


class Expense(tk.Frame):
    def __init__(self, parent=None, main=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        #Added some padding
        self.config(padx=25, pady=25)

        #Saves a reference to the root window, added "main=None" to init
        self.rootWin = main

        self.nameLabel = tk.Label(self, text="Name:")
        self.amountLabel = tk.Label(self, text="Amount (in $):")
        self.timeframeLabel = tk.Label(self, text="Timeframe:")
        self.frequencyLabel = tk.Label(self, text="Frequency:")

        self.nameData = tk.StringVar()
        self.amountData = tk.IntVar()
        self.timeframeData = tk.StringVar()

        self.timeframeData.set("Daily")
        self.frequencyData = tk.IntVar()
        self.frequencyData.set(1)

        #Added a validation command, which calls an update command to update the same data in self.account
        self.valid = self.register(self._validate)

        self.nameEntry = tk.Entry(self, textvariable=self.nameData, validate="all", validatecommand=(self.valid, "%V"))
        self.amountEntry = tk.Entry(self, textvariable=self.amountData, validate="all", validatecommand=(self.valid, "%V"))
        self.frequencyEntry = tk.Entry(self, textvariable=self.frequencyData, validate="all", validatecommand=(self.valid, "%V"))

        self.timeframeEntry = tk.OptionMenu(self, self.timeframeData, "Daily", "Weekly", "Monthly", "Yearly")
        #Trace with callback
        self.timeframeData.trace("w", self.optionUpdate)


        self.delete = tk.Button(self, text="Delete", padx=10, command=self.delete)
        self.delete.grid(row=0, column=9, sticky="NE", padx=10)

        self.nameLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")
        self.nameEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")

        self.amountLabel.grid(row=0, column=2, sticky="N"+"E"+"S"+"W")
        self.amountEntry.grid(row=0, column=3, sticky="N"+"E"+"S"+"W")

        self.timeframeLabel.grid(row=0, column=4, sticky="N"+"E"+"S"+"W")
        self.timeframeEntry.grid(row=0, column=5, sticky="N"+"E"+"S"+"W")

        self.frequencyLabel.grid(row=0, column=6, sticky="N"+"E"+"S"+"W")
        self.frequencyEntry.grid(row=0, column=7, sticky="N"+"E"+"S"+"W")

    def optionUpdate(self, *args):
        self._update()
        return

    #General update function that updates
    def _update(self):
        index = self.rootWin.expenses.index(self)
        self.rootWin.account.expenses[index].update(self.dataToList())
        return True

    def _validate(self, event):
        #Validation for user input
        if event == "focusout":
            self._update()
        return True

    def dataToList(self):
        data=[]
        #Transfers data as [name, amount, timeframe, frequency]
        data.append(self.nameData.get())
        data.append(self.amountData.get())
        data.append(self.timeframeData.get())
        data.append(self.frequencyData.get())
        return data

    def delete(self):
        index = self.rootWin.expenses.index(self)
        self.rootWin.account.expenses.pop(index)
        self.rootWin.expenses.pop(index)
        self.destroy()
        return

#Inherits from Expense class
class Income(Expense):
    #General update function that updates
    def _update(self):
        index = self.rootWin.incomes.index(self)
        self.rootWin.account.incomes[index].update(self.dataToList())
        return True

    def delete(self):
        index = self.rootWin.incomes.index(self)
        self.rootWin.account.incomes.pop(index)
        self.rootWin.incomes.pop(index)
        self.destroy()
        return

class infoGraph(tk.Frame):
    def __init__(self, parent=None, amounts=None, days=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.amounts = amounts
        self.days = days

        #Graph compenents creation
        f = Figure(figsize=(8, 7), dpi=100, frameon=False)
        a = f.add_subplot(111)
        a.set_title("Account Balance Over Time")
        a.set_ylabel("Account Balance ($)")
        a.set_xlabel("Days Elapsed")
        a.plot(self.days, self.amounts)

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        return

#The following class taken from
#https://blog.tecladocode.com/tkinter-scrollable-frames/
'''Purpose of scrollable frame is for user to be able to clearly review and add as many different expense sources and income sources as they need to'''
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=150, width=1000)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
