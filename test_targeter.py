from targeter import Targeter


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
