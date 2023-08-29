

class TodoList:
    def __init__(self):
        self.todos = []
        
    def remind_me(self, func):
        self.todos.append(func)

    def finish(self):
        for func in self.todos:
            func()
        self.clear()

    def clear(self):
        self.todos.clear()
