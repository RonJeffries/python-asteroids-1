from core.tasks import Tasks
from flyer import InvadersFlyer
from pygame import Rect, Surface
import pygame.draw_py
import u
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.ImageMasher import ImageMasher


class BottomLine(InvadersFlyer):
    def __init__(self):
        w = 960-128
        h = 4
        surface = Surface((w, h))
        surface.set_colorkey((0, 0, 0))
        surface.fill("green")
        rect = Rect(0, 0, w, h)
        rect.bottomleft = (64, u.SCREEN_SIZE - 56)
        self.position = rect.center
        self._map = surface
        self._mask = pygame.mask.from_surface(surface)
        self._rect = rect
        self._tasks = Tasks()

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self._map, self.rect)

    def begin_interactions(self, fleets):
        self._tasks.clear()

    def end_interactions(self, fleets):
        self._tasks.finish()

    def interact_with(self, other, fleets):
        other.interact_with_bottomline(self, fleets)

    def interact_with_invadershot(self, shot, fleets):
        self.process_shot_collision(shot)

    def process_shot_collision(self, shot):
        if Collider(self, shot).colliding():
            self._tasks.remind_me(lambda: self.mash_image(shot))

    def mash_image(self, shot):
        masher = ImageMasher.from_flyers(self, shot)
        masher.determine_damage()
        self._mask = masher.get_new_mask()
        masher.apply_damage_to_surface(self._map)

