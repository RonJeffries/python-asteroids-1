from todolist import TodoList


class TestTodoList:

    def save_value(self, value):
        self.value = value

    def accumulate(self, value):
        self.value += value

    def test_exists(self):
        TodoList()

    def test_remembers_things(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(17))
        todo.finish()
        assert self.value == 17

    def test_has_list(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(13))
        todo.remind_me(lambda: self.accumulate(13))
        todo.remind_me(lambda: self.accumulate(13))
        todo.finish()
        assert self.value == 39

    def test_clears_list_after_finish(self):
        todo = TodoList()
        todo.remind_me(lambda: self.save_value(31))
        todo.remind_me(lambda: self.accumulate(13))
        todo.finish()
        assert self.value == 44
        self.value = 0
        todo.finish()
        assert self.value == 0

    def test_can_clear_list(self):
        todo = TodoList()
        self.value = 0
        todo.remind_me(lambda: self.save_value(31))
        todo.clear()
        todo.finish()
        assert self.value == 0



