from View import View as v

class Controller():
    def __init__(self):
        self.view=v()
        self.view.mainloop()
    
if __name__ == "__main__":
    c = Controller()
