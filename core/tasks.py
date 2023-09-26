

class Tasks:
    def __init__(self):
        self.tasks = []
        
    def remind_me(self, func):
        self.tasks.append(func)

    def finish(self):
        for func in self.tasks:
            func()
        self.clear()

    def clear(self):
        self.tasks.clear()
