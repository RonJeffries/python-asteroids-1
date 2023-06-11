class Targeter:

    @classmethod
    def best_target(cls, shooter_coordinate, target_coordinate, screen_size):
        return Targeter(shooter_coordinate, target_coordinate, screen_size).nearest()

    def __init__(self, shooter_coordinate, target_coordinate, screen_size):
        self.target_coordinate = target_coordinate
        self.from_coordinate = shooter_coordinate
        self.size = screen_size
        self.half = self.size / 2

    def nearest(self):
        if self.target_is_near:
            return self.target_coordinate
        elif self.we_are_past_center:
            return self.target_on_high_side
        else:
            return self.target_on_low_side

    @property
    def target_is_near(self):
        return self.direct_distance <= self.half

    @property
    def direct_distance(self):
        return abs(self.target_coordinate - self.from_coordinate)

    @property
    def we_are_past_center(self):
        return self.from_coordinate >= self.half

    @property
    def target_on_high_side(self):
        return self.target_coordinate + self.size

    @property
    def target_on_low_side(self):
        return self.target_coordinate - self.size
