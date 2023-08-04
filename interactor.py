# Collider
import itertools


class Interactor:
    """
    Arrange for every object in fleets to have a chance to interact with every other.

    Given object `fred` of class `Man` and `wilma` of class `Woman`, two interaction calls will occur,
    one for `fred` and one for `wilma`:

     - `fred.interact_with_woman(wilma)`
     - `wilma.interact_with_man(fred)`

    Object `a` is free to do anything it wishes to itself.
    By convention, we might ask object `b` for information, but we generally
    do not modify it. Doubtless there are exceptions.

    Things you might do:

     - check if colliding with `b` and split or die if so (Asteroid)
     - count the object for use in later decisions (Ship)
     - notice that you don't see an object, and create one (ShipMaker)
     - observe where it is, so you can shoot at it. (Saucer)
     - ask it for its value and accumulate it. (ScoreKeeper)
    """

    def __init__(self, fleets):
        self.fleets = fleets

    def perform_interactions(self):
        self.fleets.begin_interactions()
        self.interact_all_pairs()
        self.fleets.end_interactions()

    def interact_all_pairs(self):
        for target, attacker in self.all_pairs():
            self.interact_one_pair(target, attacker)

    def all_pairs(self):
        return itertools.combinations(self.fleets.all_objects, 2)

    def interact_one_pair(self, target, attacker):
        attacker.interact_with(target, self.fleets)
        target.interact_with(attacker, self.fleets)
