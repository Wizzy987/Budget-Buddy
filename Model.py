import csv

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

    def setGoal(self, goal):
        self.goal = goal
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
    def __init__(self):
        self.account = BankAccount()

    def saveCSVFile(self, fileName):
        with open(fileName, 'w', newline='') as save:
            writer = csv.writer(save)

            writer.writerow(["Account Balance", self.account.balance])
            writer.writerow(["Budget Goal", self.account.goal])

            writer.writerow(["Type", "Name", "Amount", "Time Frame", "Frequency"])

            for expense in self.account.expenses:
                writer.writerow(["Expense", expense.name, expense.amount, expense.timeframe, expense.frequency])

            for income in self.account.incomes:
                writer.writerow(["Income", income.name, income.amount, income.timeframe, income.frequency])


    def readCSVFile(self, fileName):
        with open(fileName, 'r', newline='') as load:
            reader = csv.reader(load)
            for row in reader:
                if row[0] == "Account Balance":
                    self.account.setBalance(row[1])
                if row[0] == "Budget Goal":
                    self.account.setGoal(row[1])
                if row[0] == "Expense":
                    self.account.addExpense(Datapoint(row[1], row[2], row[3], row[4]))
                if row[0] == "Income":
                    self.account.addIncome(Datapoint(row[1], row[2], row[3], row[4]))


