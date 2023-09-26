import pygame

from flyer import InvadersFlyer


class InvaderScore(InvadersFlyer):
    def __init__(self, score):
        self.score = score

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_invaderscore(self, fleets)

    def interact_with_invaderscorekeeper(self, keeper, fleets):
        fleets.remove(self)


class InvaderScoreKeeper(InvadersFlyer):
    def __init__(self):
        self.total_score = 0
        if pygame.get_init():
            self.score_font = pygame.font.SysFont("andale mono", 48)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def draw(self, screen):
        header = "SCORE<1>"
        header_surface = self.score_font.render(header, True, "white")
        screen.blit(header_surface, (75, 10))
        score_text = f"0000{self.total_score}"[-5:]
        score_surface = self.score_font.render(score_text, True, "white")
        screen.blit(score_surface, (135, 60))

    def interact_with(self, other, fleets):
        other.interact_with_invaderscorekeeper(self, fleets)

    def interact_with_invaderscore(self, score, fleets):
        self.total_score += score.score
