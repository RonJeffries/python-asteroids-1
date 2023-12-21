from flyer import InvadersFlyer
from invaders.player_shot import PlayerShot
from invaders.raycaster import Raycaster, EmptyCastResult
from invaders.sprite import Spritely, Sprite
from pygame import Vector2
import u


class Driver(Spritely, InvadersFlyer):

    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self._sprite.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.position = Vector2(self.left, u.INVADER_PLAYER_Y)
        self.count = 0

    def nearest(self, position_vectors):
        best = position_vectors[0]
        best_dist = self.x_distance(position_vectors[0])
        for position in position_vectors:
            dist = self.x_distance(position)
            if dist < best_dist:
                best = position
                best_dist = dist
        return best

    def x_distance(self, position_vector):
        return abs(self.position.x - position_vector.x)

    def interact_with(self, other, fleets):
        other.interact_with_driver(self, fleets)

    shield_locations = ((198, 286), (378, 466), (558, 646), (738, 826))
    open_locations = ((0, 197), (287, 377), (467, 557), (647, 737), (827, 1024))

    def update(self, delta_time, fleets):
        if self._sprite.centerx < (378+286) / 2:
            centerx = self._sprite.centerx + self.step
            self.position = Vector2(centerx, self.position.y)
        self.count = (self.count + 1) % 60
        if not self.count:
            fleets.append(PlayerShot(self._sprite.center))


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
    def test_nearest_open_x(self):
        driver = Driver()
        driver.position = (500, u.INVADER_PLAYER_Y)
        x_in = (190, 290, 490, 690, 890)
        x_out = (250, 390, 590, 790)
        x_values = x_in + x_out
        y = 512
        invader_positions = [Vector2(x,y) for x in x_values]
        nearest_invader_position = driver.nearest(invader_positions)
        assert nearest_invader_position.x == 490
