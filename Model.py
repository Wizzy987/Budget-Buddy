class BankAccount():
    def __init__(self, *args):
        self.balance = 0
        self.initial_balance = 0
        self.goal = 0
        self.expenses = []
        self.incomes = []
        self.plotBalance = []
        self.plotDay = []
        
    def addExpense(self, expense):
        self.expenses.append(expense)
        return
    
    def addIncome(self, income):
        self.incomes.append(income)
        return
    
    def setBalance(self, balance):
        self.initial_balance = balance
        self.balance = balance
        return
    
    def graphBalance(self, length):
        for days in range(0, length):
            for expense in self.expenses:
                if expense.timeframe == "daily":
                    self.balance -= (expense.amount*expense.frequency)
            for income in self.incomes:
                if income.timeframe == "daily":
                    self.balance += (income.amount*income.frequency)
            if (days % 7) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "weekly":
                        self.balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "weekly":
                        self.balance += (income.amount*income.frequency)                
            if (days % 30) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "monthly":
                        self.balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "monthly":
                        self.balance += (income.amount*income.frequency)                
            self.plotBalance.append(self.balance)
            self.plotDay.append(days+1)
        return
        
        
class Datapoint():
    def __init__(self, name, amount, timeframe, frequency):
        self.name = name
        self.amount = amount
        self.timeframe = timeframe
        self.frequency = frequency
        
class Model():
    pass