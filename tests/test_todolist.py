from todolist import TodoList


class TestReminders:
    def __init__(self):
        self.value = None

    def save_value(self, value):
        self.value = value

    def test_exists(self):
        TodoList()

    def test_remembers_things(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(17))
        todo.execute()
        assert self.value == 17