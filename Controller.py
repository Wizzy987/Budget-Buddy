from View import View as v
from Model import Model as m

class Controller():
    def __init__(self):
        self.model = m()
        self.view = v(self, self.model.account)
        self.view.mainloop()
        
    def save(filename):
        self.model.saveCSVFile(filename)
        
    def load(filename):
        self.model.loadCSVFile(filename)
    
if __name__ == "__main__":
    c = Controller()
