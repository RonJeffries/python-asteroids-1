from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import Flyer
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
            invader.set_position(origin)

    def update_next(self, origin):
        if self._next_invader >= len(self.invaders):
            self._next_invader = 0
            return "end"
        invader = self.next_invader()
        invader.set_position(origin)
        self._next_invader += 1
        return "ok"

    def next_invader(self):
        return self.invaders[self._next_invader]

    def draw(self, screen):
        for invader in self.invaders:
            invader.draw(screen)

    def interact_with_bumper(self, bumper, fleet):
        for invader in self.invaders:
            invader.interact_with_bumper(bumper, fleet)

    def set_invader_position(self, index, origin):
        self.invaders[index].set_position(origin)


class InvaderFleet(Flyer):
    def __init__(self):
        self.step = Vector2(8, 0)
        self.down_step = Vector2(0, 32)

        self.invader_group = InvaderGroup()
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5*64, 512)
        self.invader_group.position_all_invaders(self.origin)
        self.reverse = False
        self.direction = 1
        self.step_origin()

    @property
    def testing_only_invaders(self):
        return self.invader_group.invaders

    def end_interactions(self, fleets):
        pass

    def update(self, delta_time, _fleets):
        result = self.invader_group.update_next(self.origin)
        self.process_result(result)

    def process_result(self, result):
        if result == "ok":
            pass
        elif result == "end":
            if self.reverse:
                self.reverse_travel()
            else:
                self.step_origin()
        else:
            assert False

    def step_origin(self):
        self.origin = self.origin + self.direction * self.step

    def reverse_travel(self):
        self.reverse = False
        self.direction = -self.direction
        self.origin = self.origin + self.direction * self.step + self.down_step


    def at_edge(self, bumper_incoming_direction):
        self.reverse = bumper_incoming_direction == self.direction

    def draw(self, screen):
        self.invader_group.draw(screen)

    def interact_with_bumper(self, bumper, _fleets):
        self.invader_group.interact_with_bumper(bumper, self)

    def interact_with(self, other, fleets):
        pass

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def tick(self, delta_time, fleets):
        pass