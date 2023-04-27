# Timer


class Timer:
    def __init__(self, delay, action, *args):
        self.delay = delay
        self.action = action
        self.args = args
        self.elapsed = 0

    def tick(self, delta_time):
        self.elapsed += delta_time
        if self.elapsed >= self.delay:
            action_complete = self.action(*self.args)
            if action_complete is None:
                raise Exception("Timer action may not return None")
            if action_complete:
                self.elapsed = 0