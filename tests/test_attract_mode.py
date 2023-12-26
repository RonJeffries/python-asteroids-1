from core.fleets import Fleets
from invaders.invader_shot import InvaderShot
from invaders.robotplayer import RobotPlayer
from invaders.raycaster import Raycaster, EmptyCastResult
import u
from invaders.sprite import Sprite
from tests.tools import FI


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
        driver = RobotPlayer()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        open_values = driver.select_values_in_open(x_values)
        assert len(open_values) == len(x_in)
        assert all([x in x_in for x in open_values])

    def test_find_nearest_open_x(self):
        driver = RobotPlayer()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        nearest_invader_x = driver.nearest_invader_x(driver.position.x, x_values)
        assert nearest_invader_x == 490

    def test_no_open(self):
        driver = RobotPlayer()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_out = (250, 390, 590, 790)
        nearest_invader_x = driver.nearest_invader_x(driver.position.x, x_out)
        assert nearest_invader_x == driver.position.x

    def test_no_invaders(self):
        driver = RobotPlayer()
        driver.position = (500, u.INVADER_PLAYER_Y)
        no_invaders = []
        nearest_invader_x = driver.nearest_invader_x(driver.position.x, no_invaders)
        assert nearest_invader_x == driver.position.x

    def test_one_step_calculation(self):
        driver = RobotPlayer()
        step = driver.step
        assert driver.one_step_toward_target(500, 400) == -step
        assert driver.one_step_toward_target(500, 600) == step
        assert driver.one_step_toward_target(500, 500) == 0

    def test_move_along_x(self):
        driver = RobotPlayer()
        driver.position = (500, u.INVADER_PLAYER_Y)
        driver.move_along_x(driver.position.x, 4)
        assert driver.position.x == 504

    def test_firing(self):
        fleets = Fleets()
        fi = FI(fleets)
        driver = RobotPlayer()
        driver.begin_interactions(fleets)
        driver.interact_with_playershot(None, fleets)
        driver.fire_when_ready(fleets)
        assert not fi.player_shots
        driver.begin_interactions(fleets)
        driver.fire_when_ready(fleets)
        assert fi.player_shots

    def test_hit_by_shot(self):
        fleets = Fleets()
        fi = FI(fleets)
        pos = (500, u.INVADER_PLAYER_Y)
        robot = RobotPlayer()
        robot.position = pos
        shot = InvaderShot(pos, Sprite.squiggles())
        robot.interact_with_invadershot(shot, fleets)
        assert not fi.robots



