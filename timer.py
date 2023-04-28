# Timer


class Timer:
    def __init__(self, delay, action, *args):
        self.delay = delay
        self.action = action
        self.args = args
        self.elapsed = 0

    def tick(self, delta_time, *tick_args):
        self.elapsed += delta_time
        if self.elapsed >= self.delay:
            action_complete = self.action(*self.args, *tick_args)
            if action_complete is None or action_complete:
                self.elapsed = 0
