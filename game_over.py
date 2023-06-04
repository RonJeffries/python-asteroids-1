import pygame

import u
from flyer import Flyer


class GameOver(Flyer):
    def __init__(self):
        self.init_game_over()

    # noinspection PyAttributeOutsideInit
    def init_game_over(self):
        if not pygame.get_init():
            return
        big_font = pygame.font.SysFont("arial", 64)
        small_font = pygame.font.SysFont("arial", 48)
        self.game_over_surface = big_font.render("GAME OVER", True, "white")
        self.game_over_pos = self.game_over_surface.get_rect(centerx=u.CENTER.x, centery=u.CENTER.y / 2)
        pos_left = u.CENTER.x - 150
        pos_top = self.game_over_pos.centery
        self.help_lines = []
        messages = ["d - turn left", "f - turn right", "j - accelerate", "k - fire missile", "q - insert quarter", ]
        for message in messages:
            pos_top += 60
            text = small_font.render(message, True, "white")
            text_rect = text.get_rect(topleft=(pos_left, pos_top))
            pair = (text, text_rect)
            self.help_lines.append(pair)

    def draw(self, screen):
        screen.blit(self.game_over_surface, self.game_over_pos)
        for text, pos in self.help_lines:
            screen.blit(text, pos)

    def interact_with(self, other, fleets):
        other.interact_with_gameover(self, fleets)

    def tick(self, delta_time, _fleet, _fleets):
        pass
