import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class View(tk.Tk):
    """Applications root window"""

    def __init__(self, controller=None, account=None, *config):
        """Code goes here"""
        tk.Tk.__init__(self, *config)

        self.title("Budget Buddy")

        self.controller = controller

        self.account = account

        #Below is code for the motherFrame
        self.motherFrame = tk.Frame(self)
        self.motherFrame.grid(row=0, column=0, columnspan=7)
        #Need to add all frame classes for each feature into motherFrame

        #Test GUI for graph timeframe
        self.timeframeLabel = tk.Label(self, text="Select Time Interval:")
        self.timeframe = tk.StringVar()
        self.timeframe.set("Day")
        self.timeframeMenu = tk.OptionMenu(self, self.timeframe, "Day", "Week", "Month", "Year")
        self.timeframeLabel.grid(row=2, column=0, sticky="NSEW")
        self.timeframeMenu.grid(row=2, column=1, sticky="NSEW")

        self.repeatsLabel = tk.Label(self, text="Repeat Interval:")
        self.repeats = tk.IntVar()
        self.repeats.set(1)
        self.repeatsBTN = tk.Entry(self, textvariable=self.repeats)
        self.repeatsLabel.grid(row=2, column=2, sticky="NSEW")
        self.repeatsBTN.grid(row=2, column=3, sticky="NSEW")

        self.graphBTN = tk.Button(self, text="Graph", padx=25, pady=15, command=self.graph)
        self.graphBTN.grid(row=3, column=0, columnspan=2, sticky="NSEW")

        #Test GUI for output values
        self.initialBalanceOutput = tk.IntVar()
        self.finalBalanceOutput = tk.IntVar()
        self.netOutput = tk.IntVar()
        self.goalOutput = tk.IntVar()

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

        #Test GUI frames for save/load GUI
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

        #Menu Stuff
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
        f = filedialog.asksaveasfilename()
        if f:
            self.controller.save(f)
            messagebox.showinfo("File Save", "Budget saved to " + f)
        return

    def load(self):
        response = messagebox.askyesno("Loading New File", "All unsaved changes will be lost. Load a budget from file?")
        if response:
            f = filedialog.askopenfilename()
            if f:
                #Calls the load function in controller.
                self.controller.load(f)

                #Sets the balance info to the account balance entries
                self.accountBalanceFrame.currentBalanceData.set(self.account.balance)
                self.accountBalanceFrame.goalBalanceData.set(self.account.goal)

                #Destroys/Deletes the current income/expense frames in the window.
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

                    self.expenses[index].nameExpenseData.set(self.account.expenses[index].name)
                    self.expenses[index].amountExpenseData.set(self.account.expenses[index].amount)
                    self.expenses[index].timeframeExpenseData.set(self.account.expenses[index].timeframe)
                    self.expenses[index].frequencyExpenseData.set(self.account.expenses[index].frequency)


                for index in range(0, len(self.account.incomes)):
                    new = Income(self.incomeFrame.scrollable_frame, self, pady=25, padx=25)
                    self.incomes.append(new)
                    new.pack(side="top", expand="TRUE", fill="both")

                    self.incomes[index].nameIncomeData.set(self.account.incomes[index].name)
                    self.incomes[index].amountIncomeData.set(self.account.incomes[index].amount)
                    self.incomes[index].timeframeIncomeData.set(self.account.incomes[index].timeframe)
                    self.incomes[index].frequencyIncomeData.set(self.account.incomes[index].frequency)

                #A dialog showing that the requested file has been loaded
                messagebox.showinfo("File Load", f + " Loaded")
        return

    def lengthInDays(self):
        if self.timeframe.get() == "Day":
            return 1 * self.repeats.get()
        elif self.timeframe.get() == "Week":
            return 7 * self.repeats.get()
        elif self.timeframe.get() == "Month":
            return 30 * self.repeats.get()
        elif self.timeframe.get() == "Year":
            return 365 * self.repeats.get()

    def graph(self):
        self.graphBTN.focus_set()

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
        self.finalBalanceOutput.set(self.account.balance)
        self.netOutput.set(self.account.getNetOutput())
        self.goalOutput.set(self.account.getGoalOutput())
        return

    def addExpenseFrame(self):

        #Instantiated a new Expense as new
        new = Expense(self.expenseFrame.scrollable_frame, self, pady=25, padx=25)
        #Adds new to the list of expenses
        self.expenses.append(new)

        #Adds new to the model
        self.account.addExpense([new.nameExpenseData.get(), new.amountExpenseData.get(), new.timeframeExpenseData.get(), new.frequencyExpenseData.get()])

        #Grids the expense frame onto the window
        new.pack(side="top", expand="TRUE", fill="both")
        return

    def addIncomeFrame(self):
        new = Income(self.incomeFrame.scrollable_frame, self, pady=25, padx=25)
        self.incomes.append(new)

        self.account.addIncome([new.nameIncomeData.get(), new.amountIncomeData.get(), new.timeframeIncomeData.get(), new.frequencyIncomeData.get()])

        new.pack(side="top", expand="TRUE", fill="both")
        return

class currentAndGoalBalance(tk.Frame):
    def __init__(self, parent=None, main=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        self.rootWin = main

        self.currentBalanceData = tk.IntVar()
        self.goalBalanceData = tk.IntVar()
        #^[P.S.:]Keep in mind we may have to change these to StringVar's if we want our users to see commas just for better use
        #If we end up implementing this, code for adding decimal point at index[-3] and index[-2:].isdigit(), then add commas /
        #automatically after three numbers inputted
        #In order to convert these to integers, split the commas and add it to one net float value

        '''^What do you guys think?'''

        self.currentBalanceLabel = tk.Label(self, text="Current Balance:")
        self.currentBalanceLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")

        self.valid = self.register(self._validate)

        #Remember to add _update on these entries like the ones below
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
        #if event == "key":
            #print(event)
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

        #Suggestion: Rename these variable so that: 1. they'll be infinitely easier to type out (cause I'm into copy paste but it's still annoying)
        #and 2. it'll be easier to make income inherit from this class so that it's easier to just edit income
        self.nameExpenseLabel = tk.Label(self, text="Name")
        self.amountExpenseLabel = tk.Label(self, text="Amount")
        self.timeframeExpenseLabel = tk.Label(self, text="Timeframe")
        self.frequencyExpenseLabel = tk.Label(self, text="Frequency")

        self.nameExpenseData = tk.StringVar()
        self.amountExpenseData = tk.IntVar()
        self.timeframeExpenseData = tk.StringVar()

        self.timeframeExpenseData.set("Daily")
        self.frequencyExpenseData = tk.IntVar()
        self.frequencyExpenseData.set(1)

        #Added a validation command, which calls an update command to update the same data in self.account
        self.valid = self.register(self._validate)

        self.nameExpenseEntry = tk.Entry(self, textvariable=self.nameExpenseData, validate="all", validatecommand=(self.valid, "%V"))
        self.amountExpenseEntry = tk.Entry(self, textvariable=self.amountExpenseData, validate="all", validatecommand=(self.valid, "%V"))
        self.frequencyExpenseEntry = tk.Entry(self, textvariable=self.frequencyExpenseData, validate="all", validatecommand=(self.valid, "%V"))

        #Option Menu is a bit trickier to implement with an update command, so it doesn't have a validate
        self.timeframeExpenseEntry = tk.OptionMenu(self, self.timeframeExpenseData, "Daily", "Weekly", "Monthly", "Yearly")
        #Instead we just use trace, with a callback
        self.timeframeExpenseData.trace("w", self.optionUpdate)


        self.delete = tk.Button(self, text="Delete", padx=10, command=self.delete)
        self.delete.grid(row=0, column=9, sticky="NE", padx=10)

        self.nameExpenseLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")
        self.nameExpenseEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")

        self.amountExpenseLabel.grid(row=0, column=2, sticky="N"+"E"+"S"+"W")
        self.amountExpenseEntry.grid(row=0, column=3, sticky="N"+"E"+"S"+"W")

        self.timeframeExpenseLabel.grid(row=0, column=4, sticky="N"+"E"+"S"+"W")
        self.timeframeExpenseEntry.grid(row=0, column=5, sticky="N"+"E"+"S"+"W")

        self.frequencyExpenseLabel.grid(row=0, column=6, sticky="N"+"E"+"S"+"W")
        self.frequencyExpenseEntry.grid(row=0, column=7, sticky="N"+"E"+"S"+"W")

    def optionUpdate(self, *args):
        self._update()
        return

    #General update function that updates
    def _update(self):
        index = self.rootWin.expenses.index(self)
        self.rootWin.account.expenses[index].update(self.dataToList())
        return True

    def _validate(self, event):
        #if event == "key":
            #print(event)
        if event == "focusout":
            self._update()
        return True

    def dataToList(self):
        data=[]
        #Transfers data as [name, amount, timeframe, frequency]
        data.append(self.nameExpenseData.get())
        data.append(self.amountExpenseData.get())
        data.append(self.timeframeExpenseData.get())
        data.append(self.frequencyExpenseData.get())
        return data

    def delete(self):
        index = self.rootWin.expenses.index(self)
        self.rootWin.account.expenses.pop(index)
        self.rootWin.expenses.pop(index)
        self.destroy()
        return


#Make this class inherit from Expense. It'll make it easier
#^ADDENDUM: Not sure exactly what you mean, good news is it appears the GUI is working as intended with this code
##reference the week 5 lecture slides, since that has all the inheritance stuff in it.
##inheritance makes the Income class inherit all the methods from Expense. would also allow you to use a generic __init__ so that we only need one
class Income(tk.Frame):
    def __init__(self, parent=None, main=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        #Saves a reference to the root window, added "main=None" to init
        self.rootWin = main

        self.nameIncomeLabel = tk.Label(self, text="Name")
        self.amountIncomeLabel = tk.Label(self, text="Amount")
        self.timeframeIncomeLabel = tk.Label(self, text="Timeframe")
        self.frequencyIncomeLabel = tk.Label(self, text="Frequency")

        self.nameIncomeData = tk.StringVar()
        self.amountIncomeData = tk.IntVar()
        self.timeframeIncomeData = tk.StringVar()
        self.timeframeIncomeData.set("Daily")
        self.frequencyIncomeData = tk.IntVar()
        self.frequencyIncomeData.set(1)

        #Added a validation command, which calls an update command to update the same data in self.account
        self.valid = self.register(self._validate)

        self.nameIncomeEntry = tk.Entry(self, textvariable=self.nameIncomeData, validate="all", validatecommand=(self.valid, "%V"))
        self.amountIncomeEntry = tk.Entry(self, textvariable=self.amountIncomeData, validate="all", validatecommand=(self.valid, "%V"))
        self.frequencyIncomeEntry = tk.Entry(self, textvariable=self.frequencyIncomeData, validate="all", validatecommand=(self.valid, "%V"))

        #Option Menu is a bit trickier to implement with an update command, so it doesn't have a validate
        self.timeframeIncomeEntry = tk.OptionMenu(self, self.timeframeIncomeData, "Daily", "Weekly", "Monthly", "Yearly")
        #Instead we just use trace, with a callback
        self.timeframeIncomeData.trace("w", self.optionUpdate)

        self.delete = tk.Button(self, text="Delete", padx=10, command=self.delete)
        self.delete.grid(row=0, column=9, sticky="NE", padx=10)

        self.nameIncomeLabel.grid(row=0, column=0, sticky="N"+"E"+"S"+"W")
        self.nameIncomeEntry.grid(row=0, column=1, sticky="N"+"E"+"S"+"W")

        self.amountIncomeLabel.grid(row=0, column=2, sticky="N"+"E"+"S"+"W")
        self.amountIncomeEntry.grid(row=0, column=3, sticky="N"+"E"+"S"+"W")

        self.timeframeIncomeLabel.grid(row=0, column=4, sticky="N"+"E"+"S"+"W")
        self.timeframeIncomeEntry.grid(row=0, column=5, sticky="N"+"E"+"S"+"W")

        self.frequencyIncomeLabel.grid(row=0, column=6, sticky="N"+"E"+"S"+"W")
        self.frequencyIncomeEntry.grid(row=0, column=7, sticky="N"+"E"+"S"+"W")

    def optionUpdate(self, *args):
        self._update()
        return

    #General update function that updates
    def _update(self):
        index = self.rootWin.incomes.index(self)
        self.rootWin.account.incomes[index].update(self.dataToList())
        return True

    def _validate(self, event):
        #if event == "key":
            #print(event)
        if event == "focusout":
            self._update()
        return True

    def dataToList(self):
        data=[]
        #Transfers data as [name, amount, timeframe, frequency]
        data.append(self.nameIncomeData.get())
        data.append(self.amountIncomeData.get())
        data.append(self.timeframeIncomeData.get())
        data.append(self.frequencyIncomeData.get())
        return data

    def delete(self):
        index = self.rootWin.incomes.index(self)
        self.rootWin.account.incomes.pop(index)
        self.rootWin.incomes.pop(index)
        self.destroy()
        return

class infoGraph(tk.Frame):
    def __init__(self, parent=None, amounts=None, days=None, **configs):
        tk.Frame.__init__(self, parent, **configs)

        #[Code here] for mathlib and pandas interaction for graph to appear
        #May need to make an additional frame for displaying the graph, unsure at this current time

        self.amounts = amounts
        self.days = days

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
