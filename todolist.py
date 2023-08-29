

class TodoList:
    def __init__(self):
        self.todos = []
        
    def remind_me(self, func):
        self.todos.append(func)

    def execute(self):
        for func in self.todos:
            func()
        self.todos.clear()
