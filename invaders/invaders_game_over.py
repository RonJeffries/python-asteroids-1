from flyer import InvadersFlyer
import pygame
import u


class InvadersGameOver(InvadersFlyer):
    def __init__(self):
        self.init_game_over()

    # noinspection PyAttributeOutsideInit
    def init_game_over(self):
        if not pygame.get_init():
            return
        big_font = pygame.font.SysFont("arial", 64)
        self.game_over_surface = big_font.render("GAME OVER", True, "white")
        self.game_over_pos = self.game_over_surface.get_rect(centerx=u.CENTER.x, centery=u.CENTER.y / 2)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_withinvadersgameover(self, fleets)

    def draw(self, screen):
        screen.blit(self.game_over_surface, self.game_over_pos)
