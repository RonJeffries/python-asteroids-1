from todolist import TodoList


class TestReminders:
    def __init__(self):
        self.value = None
        self.total = 0

    def save_value(self, value):
        self.value = value

    def accumulate(self, value):
        self.total += value

    def test_exists(self):
        TodoList()

    def test_remembers_things(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(17))
        todo.execute()
        assert self.value == 17

    def test_has_list(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(86))
        todo.remind_me(lambda: self.accumulate(13))
        todo.remind_me(lambda: self.accumulate(13))
        todo.execute()
        assert self.value == 86
        assert self.total == 26
