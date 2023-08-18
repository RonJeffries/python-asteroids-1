from bitmap_maker import BitmapMaker
from invader import Invader


class InvaderGroup():
    def __init__(self):
        self.invaders = []
        invader_table = self.create_invader_bitmaps()
        self.create_invaders(invader_table)
        self._next_invader = 0

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

    def update_next(self, origin):
        if self._next_invader >= len(self.invaders):
            self._next_invader = 0
            return "end"
        invader = self.next_invader()
        invader.position = origin
        self._next_invader += 1
        return "ok"

    def next_invader(self):
        return self.invaders[self._next_invader]

    def draw(self, screen):
        # image.fill("red", rect, special_flags=pygame.BLEND_MULT)
        for invader in self.invaders:
            invader.draw(screen)

    def interact_with_bumper(self, bumper, fleet):
        for invader in self.invaders:
            invader.interact_with_bumper(bumper, fleet)

    def interact_with_playershot(self, shot, fleets):
        for invader in self.invaders.copy():
            invader.interact_with_group_and_playershot(shot, self, fleets)

    def set_invader_position(self, index, origin):
        self.invaders[index].set_position(origin)
