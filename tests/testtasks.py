from core.tasks import Tasks


class TestTasks:

    def save_value(self, value):
        self.value = value

    def accumulate(self, value):
        self.value += value

    def test_exists(self):
        Tasks()

    def test_remembers_things(self):
        tasks = Tasks()
        tasks.remind_me(lambda: self.save_value(17))
        tasks.finish()
        assert self.value == 17

    def test_has_list(self):
        tasks = Tasks()
        tasks.remind_me(lambda: self.save_value(13))
        tasks.remind_me(lambda: self.accumulate(13))
        tasks.remind_me(lambda: self.accumulate(13))
        tasks.finish()
        assert self.value == 39

    def test_clears_list_after_finish(self):
        tasks = Tasks()
        tasks.remind_me(lambda: self.save_value(31))
        tasks.remind_me(lambda: self.accumulate(13))
        tasks.finish()
        assert self.value == 44
        self.value = 0
        tasks.finish()
        assert self.value == 0

    def test_can_clear_list(self):
        tasks = Tasks()
        self.value = 0
        tasks.remind_me(lambda: self.save_value(31))
        tasks.clear()
        tasks.finish()
        assert self.value == 0



