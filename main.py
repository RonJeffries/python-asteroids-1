# Asteroids Main program
from fleet import ShipFleet
from game import Game

asteroids_game: Game

if __name__ == "__main__":
    keep_going = True
    ShipFleet.rez_from_fleet = False
    while keep_going:
        asteroids_game = Game()
        keep_going = asteroids_game.main_loop()
