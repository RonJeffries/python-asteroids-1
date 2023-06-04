import pygame

from flyer import Flyer


class ScoreKeeper(Flyer):
    def __init__(self):
        self.score = 0
        if pygame.get_init():
            self.score_font = pygame.font.SysFont("arial", 48)

    @staticmethod
    def are_we_colliding(_position, _radius):
        return False

    def draw(self, screen):
        score_surface, score_rect = self.render_score()
        screen.blit(score_surface, score_rect)

    def render_score(self):
        score_text = f"0000{self.score}"[-5:]
        score_surface = self.score_font.render(score_text, True, "green")
        score_rect = score_surface.get_rect(topleft=(10, 10))
        return score_surface, score_rect

    def interact_with(self, other, fleets):
        other.interact_with_scorekeeper(self, fleets)

    def interact_with_score(self, score, fleets):
        self.score += score.score

    def tick(self, delta_time, _fleet, _fleets):
        pass
