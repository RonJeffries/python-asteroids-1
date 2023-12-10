from enum import Enum

import u
from invaders.bitmap_maker import BitmapMaker
from invaders.invader import Invader
from invaders.sprite import Sprite


class CycleStatus(Enum):
    CONTINUE = "continue"
    NEW_CYCLE = "new cycle"
    REVERSE = "reverse"


class InvaderGroup:
    def __init__(self):
        self.invaders = []
        self.create_invaders()
        self._next_invader = 0

    def testing_set_to_end(self):
        self._next_invader = len(self.invaders)

    def bottom_of_column(self, column):
        matching = [invader for invader in self.invaders if invader.column == column]
        return matching[0] if matching else None

    def invader_count(self):
        return len(self.invaders)

    def kill(self, invader):
        index = self.invaders.index(invader)
        self.invaders.pop(index)
        if self._next_invader > index:
            self._next_invader -= 1

    def create_invaders(self):
        self.invaders = []
        for x in range(55):
            col = x % 11
            row = x // 11
            sprite = Sprite.invader(row)
            self.invaders.append(Invader(col, row, sprite))

    def position_all_invaders(self, origin):
        for invader in self.invaders:
            invader.move_relative_to(origin)

    def update_next(self, origin):
        return self.perform_update_step(origin)

    def perform_update_step(self, origin):
        if self._next_invader < len(self.invaders):
            self.move_one_invader(origin)
            return CycleStatus.CONTINUE
        else:
            return self.end_cycle()

    def move_one_invader(self, origin):
        invader = self.next_invader()
        invader.move_relative_to(origin)
        self._next_invader += 1

    def end_cycle(self):
        self._next_invader = 0
        return CycleStatus.REVERSE if self.any_out_of_bounds() else CycleStatus.NEW_CYCLE

    def next_invader(self):
        return self.invaders[self._next_invader]

    def draw(self, screen):
        # image.fill("red", rect, special_flags=pygame.BLEND_MULT)
        for invader in self.invaders:
            invader.draw(screen)

    def any_out_of_bounds(self):
        left = u.BUMPER_LEFT + u.INVADER_HALF_WIDTH
        right = u.BUMPER_RIGHT - u.INVADER_HALF_WIDTH
        colliding = [invader.is_out_of_bounds(left, right) for invader in self.invaders]
        return any(colliding)

    def interact_with_playershot(self, shot, fleets):
        for invader in self.invaders.copy():
            invader.interact_with_group_and_playershot(shot, self, fleets)

    def interact_with_roadfurniture(self, shield, fleets):
        for invader in self.invaders.copy():
            invader.interact_with_roadfurniture(shield, fleets)
