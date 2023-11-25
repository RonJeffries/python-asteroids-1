from enum import Enum

from invaders.bitmap_maker import BitmapMaker
from invaders.invader import Invader


class CycleStatus(Enum):
    CONTINUE = "continue"
    NEW_CYCLE = "new cycle"
    REVERSE = "reverse"

class InvaderGroup():
    def __init__(self):
        self.invaders = []
        invader_table = self.create_invader_bitmaps()
        self.create_invaders(invader_table)
        self._next_invader = 0
        self.current_direction = 1
        self.should_reverse = False

    def testing_set_to_end(self):
        self._next_invader = len(self.invaders)

    def create_invader_bitmaps(self):
        maker = BitmapMaker.instance()
        aliens = maker.invaders
        alien_table = (aliens[0:2], aliens[0:2], aliens[2:4], aliens[2:4], aliens[4:])
        return alien_table

    def bottom_of_column(self, column):
        matching = [invader for invader in self.invaders if invader.column == column]
        if matching:
            return matching[0]
        else:
            return None

    def invader_count(self):
        return len(self.invaders)

    def kill(self, invader):
        index = self.invaders.index(invader)
        self.invaders.pop(index)
        if self._next_invader > index:
            self._next_invader -= 1

    def create_invaders(self, invader_table):
        self.invaders = []
        for x in range(55):
            col = x % 11
            row = x // 11
            maps = invader_table[row]
            self.invaders.append(Invader(col, row, maps))

    def position_all_invaders(self, origin):
        for invader in self.invaders:
            invader.position = origin

    def update_next(self, origin, current_direction):
        self.handle_direction_change(current_direction)
        return self.perform_update_step(origin)

    def handle_direction_change(self, current_direction):
        if self.current_direction != current_direction:
            self.current_direction = current_direction

    def perform_update_step(self, origin):
        if self._next_invader < len(self.invaders):
            self.move_one_invader(origin)
            return CycleStatus.CONTINUE
        else:
            return self.end_cycle()

    def move_one_invader(self, origin):
        invader = self.next_invader()
        invader.position = origin
        self._next_invader += 1

    def end_cycle(self):
        self._next_invader = 0
        return CycleStatus.REVERSE if self.should_reverse else CycleStatus.NEW_CYCLE

    def next_invader(self):
        return self.invaders[self._next_invader]

    def draw(self, screen):
        # image.fill("red", rect, special_flags=pygame.BLEND_MULT)
        for invader in self.invaders:
            invader.draw(screen)
        # surf = BitmapMaker.instance().player_shot_explosion
        # rect = surf.get_rect()
        # rect.center = (100, 900)
        # screen.blit(surf, rect)
        # pygame.draw.line(screen, "red", (100, 850), (100, 950))
        # pygame.draw.line(screen, "red", (50, 900), (150, 900))

    def begin_interactions(self, fleets):
        self.should_reverse = False

    def interact_with_bumper(self, bumper, _fleet):
        if self._next_invader < len(self.invaders):
            return
        colliding = [invader.is_entering(bumper, self.current_direction) for invader in self.invaders]
        self.should_reverse |= any(colliding)

    def interact_with_playershot(self, shot, fleets):
        for invader in self.invaders.copy():
            invader.interact_with_group_and_playershot(shot, self, fleets)
