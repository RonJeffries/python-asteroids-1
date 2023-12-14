from pygame import Vector2

import u
from flyer import InvadersFlyer
from invaders.invader_group import InvaderGroup, CycleStatus
from invaders.timecapsule import TimeCapsule


class InvaderFleet(InvadersFlyer):

    step = Vector2(8, 0)
    down_step = Vector2(0, 32)

    def __init__(self, generator=None):
        if generator is None:
            def generate_y():
                def convert(y_8080):
                    return 0x400 - 4*y_8080
                yield convert(u.INVADER_FIRST_START)
                index = 0
                while True:
                    yield convert(u.INVADER_STARTS[index])
                    index = (index + 1) % len(u.INVADER_STARTS)

            generator = generate_y()
        self.y_generator = generator
        y = next(self.y_generator)
        self.origin = Vector2(u.SCREEN_SIZE / 2 - 5 * 64, y)
        self.invader_group = InvaderGroup()
        self.invader_group.position_all_invaders(self.origin)
        self.direction = 1
        self.step_origin()

    def next_fleet(self):
        return InvaderFleet(self.y_generator)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    @property
    def testing_only_invaders(self):
        return self.invader_group.invaders

    def invader_count(self):
        return self.invader_group.invader_count()

    @staticmethod
    def convert_y_coordinate(y_on_8080):
        return 0x400 - 4*y_on_8080

    def update(self, delta_time, _fleets):
        result = self.invader_group.update_next(self.origin)
        self.process_result(result, _fleets)

    def process_result(self, result, fleets):
        if result == CycleStatus.CONTINUE:
            pass
        elif result == CycleStatus.NEW_CYCLE:
            self.step_origin()
        elif result == CycleStatus.REVERSE:
            self.reverse_travel()
        elif result == CycleStatus.EMPTY:
            fleets.remove(self)
            capsule = TimeCapsule(2, self.next_fleet())
            fleets.append(capsule)

    def step_origin(self):
        self.origin = self.origin + self.direction * self.step

    def reverse_travel(self):
        self.direction = -self.direction
        self.origin = self.origin + self.direction * self.step + self.down_step

    def draw(self, screen):
        self.invader_group.draw(screen)

    def interact_with_invaderplayer(self, player, fleets):
        self.invader_group.interact_with_invaderplayer(player,fleets)

    def interact_with_roadfurniture(self, shield, fleets):
        self.invader_group.interact_with_roadfurniture(shield, fleets)

    def interact_with_playershot(self, shot, fleets):
        self.invader_group.interact_with_playershot(shot, fleets)

    def interact_with(self, other, fleets):
        other.interact_with_invaderfleet(self, fleets)


class StartingHelper:
    @property
    def starting_8080_y(self):
        return u.INVADER_FIRST_START

    @property
    def next_index(self):
        return 0


class RunningHelper:
    def __init__(self, index):
        self.index = index % len(u.INVADER_STARTS)

    @property
    def starting_8080_y(self):
        return u.INVADER_STARTS[self.index]

    @property
    def next_index(self):
        return (self.index + 1) % len(u.INVADER_STARTS)


class OriginHelper:
    @classmethod
    def make_helper(cls, start):
        if start is None:
            return StartingHelper()
        else:
            return RunningHelper(start)

