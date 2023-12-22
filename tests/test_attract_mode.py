from invaders.driver import Driver
from invaders.raycaster import Raycaster, EmptyCastResult
import u


class TestAttractMode:
    def test_hookup(self):
        assert 2+2 == 4

    def test_raycaster_exists(self):
        Raycaster()

    def test_empty_scan(self):
        caster = Raycaster()
        x = 15
        result = caster.cast(x)
        assert isinstance(result, EmptyCastResult)

    # open_locations = ((0, 197), (287, 377), (467, 557), (647, 737), (827, 1024))
    def test_find_open_xs(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        open_values = driver.select_values_in_open(x_values)
        assert len(open_values) == len(x_in)
        assert all([x in x_in for x in open_values])

    def test_find_nearest_open_x(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        nearest_invader_x = driver.nearest_invader_x(x_values)
        assert nearest_invader_x == 490

    def test_no_open(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_out = (250, 390, 590, 790)
        nearest_invader_x = driver.nearest_invader_x(x_out)
        assert nearest_invader_x == driver.position.x

    def test_no_invaders(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        no_invaders = []
        nearest_invader_x = driver.nearest_invader_x(no_invaders)
        assert nearest_invader_x == driver.position.x


