# Fleet

class Fleet:
    def __init__(self, flyers):
        self.flyers = flyers

    def __iter__(self):
        return self.flyers.copy().__iter__()

    def append(self, flyer):
        self.flyers.append(flyer)

    def remove(self, flyer):
        if flyer in self.flyers: self.flyers.remove(flyer)

    def draw(self, screen):
        for flyer in self:
            flyer.draw(screen)

    def move(self, delta_time):
        for flyer in self:
            flyer.move(delta_time, self)

    def tick(self, delta_time):
        return True
