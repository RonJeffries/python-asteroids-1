

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


class TestTargeter:

    def test_can_choose_nearest_scalar_target(self):
        target = 100
        screen_size = 500
        shooter = 200
        assert Targeter(shooter, target, screen_size).nearest() == 100
        shooter = 400
        assert Targeter(shooter, target, screen_size).nearest() == 100 + 500
        target = 400
        shooter = 100
        assert Targeter(shooter, target, screen_size).nearest() == 400 - 500

    def test_best_target(self):
        target = 100
        screen_size = 500
        shooter = 200
        assert Targeter.best_target(shooter, target, screen_size) == 100
        shooter = 400
        assert Targeter.best_target(shooter, target, screen_size) == 100 + 500
        target = 400
        shooter = 100
        assert Targeter.best_target(shooter, target, screen_size) == 400 - 500
