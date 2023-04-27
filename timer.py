# Timer


class Timer:
    def __init__(self, delay, action):
        self.delay = delay
        self.action = action
        self.elapsed = 0

    def tick(self, delta_time):
        self.elapsed += delta_time
        if self.elapsed >= self.delay:
            action_complete = self.action()
            if action_complete == None:
                raise Exception("Timer action may not return None")
            if action_complete:
                self.elapsed = 0