import csv

class BankAccount():
    def __init__(self, *args):
        #Starting and dynamic variables used for calculations and graphing
        self.balance = 0
        self.initial_balance = 0
        self.goal = 0
        self.expenses = []
        self.incomes = []
        self.plotBalance = []
        self.plotDay = []

    def clear(self):
        #Function to reset starting/dynamic variables to empty
        self.balance = 0
        self.initial_balance = 0
        self.goal = 0
        self.expenses = []
        self.incomes = []
        self.plotBalance = []
        self.plotDay = []
        return

    def addExpense(self, dataList):
        expense = Datapoint(dataList[0], dataList[1], dataList[2], dataList[3])
        self.expenses.append(expense)
        return

    def addIncome(self, dataList):
        income = Datapoint(dataList[0], dataList[1], dataList[2], dataList[3])
        self.incomes.append(income)
        return

    def setBalance(self, balance):
        self.initial_balance = int(balance)
        self.balance = int(balance)
        return

    def setGoal(self, goal):
        self.goal = goal
        return

    def getNetOutput(self):
        net = int(self.plotBalance[len(self.plotBalance) - 1]) - int(self.initial_balance)
        return net

    def getGoalOutput(self):
        goal = int(self.plotBalance[len(self.plotBalance) - 1]) - int(self.goal)
        return goal

    def graphBalance(self, length):
        #Formulas determining time (x-axis) on the graph depending on user selection
        balance = self.balance
        for days in range(0, length):
            '''for expense in self.expenses:
                if expense.timeframe == "Daily":
                    balance -= (expense.amount*expense.frequency)
            for income in self.incomes:
                if income.timeframe == "Daily":
                    balance += (income.amount*income.frequency)'''
            if (days % 365) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "Yearly":
                        balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "Yearly":
                        balance += (income.amount*income.frequency)
            elif (days % 30) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "Monthly":
                        balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "Monthly":
                        balance += (income.amount*income.frequency)
            elif (days % 7) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "Weekly":
                        balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "Weekly":
                        balance += (income.amount*income.frequency)
            elif (days % 1) == 0:
                for expense in self.expenses:
                    if expense.timeframe == "Daily":
                        balance -= (expense.amount*expense.frequency)
                for income in self.incomes:
                    if income.timeframe == "Daily":
                        balance += (income.amount*income.frequency)
            self.plotBalance.append(balance)
            self.plotDay.append(days+1)
        return

    def getPlotBalance(self):
        points = []
        for point in self.plotBalance:
            points.append(point)
        return points

    def getPlotDay(self):
        days = []
        for day in self.plotDay:
            days.append(day)
        return days

class Datapoint():
    def __init__(self, name, amount, timeframe, frequency):
        self.name = name
        self.amount = amount
        self.timeframe = timeframe
        self.frequency = frequency

    def update(self, data):
        self.name = data[0]
        self.amount = data[1]
        self.timeframe = data[2]
        self.frequency = data[3]

    def get(self):
        print("Name:" + self.name)
        print("Amount:", self.amount)
        print("Frame:", self.timeframe)
        print("Frequency:", self.frequency)


class Model():
    def __init__(self):
        self.account = BankAccount()

    def saveCSVFile(self, fileName):
        #Function for saving budget layout for easy reopening and reviewing budgeting graph. Only .csv (Excel) files are allowed to be saved
        with open(fileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(["Account Balance", self.account.balance])
            writer.writerow(["Budget Goal", self.account.goal])

            writer.writerow(["Type", "Name", "Amount", "Time Frame", "Frequency"])

            for expense in self.account.expenses:
                writer.writerow(["Expense", expense.name, expense.amount, expense.timeframe, expense.frequency])

            for income in self.account.incomes:
                writer.writerow(["Income", income.name, income.amount, income.timeframe, income.frequency])


    def readCSVFile(self, fileName):
        #Function for loading budget layout for ability to reference saved budget layouts. Account is cleared to prevent conflicts. Only .csv (Excel) files allowed to load
        self.account.clear()
        with open(fileName, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[0] == "Account Balance":
                    self.account.setBalance(row[1])
                if row[0] == "Budget Goal":
                    self.account.setGoal(row[1])
                if row[0] == "Expense":
                    print("We loading this:", row[4])
                    self.account.addExpense([row[1], row[2], row[3], row[4]])
                if row[0] == "Income":
                    self.account.addIncome([row[1], row[2], row[3], row[4]])


