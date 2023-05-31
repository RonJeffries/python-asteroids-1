# Fleet


class Fleet:
    def __init__(self, flyers):
        self.flyers = flyers

    def __bool__(self):
        return bool(self.flyers)

    def __iter__(self):
        return self.flyers.copy().__iter__()

    def __len__(self):
        return len(self.flyers)

    def __getitem__(self, item):
        return self.flyers[item]

    def append(self, flyer):
        self.flyers.append(flyer)

    def clear(self):
        self.flyers.clear()

    def extend(self, list_of_flyers):
        self.flyers.extend(list_of_flyers)

    def remove(self, flyer):
        if flyer in self.flyers:
            self.flyers.remove(flyer)

    def draw(self, screen):
        for flyer in self:
            flyer.draw(screen)

    def move(self, delta_time, fleets):
        for flyer in self:
            flyer.move(delta_time, fleets)

    def tick(self, delta_time, fleets):
        for flyer in self:
            flyer.tick(delta_time, self, fleets)

