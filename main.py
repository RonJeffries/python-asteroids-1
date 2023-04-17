# Asteroids Main program

from game import Game

asteroids_game: Game

if __name__ == "__main__":
    asteroids_game = Game()
    asteroids_game.set_instance(asteroids_game)
    asteroids_game.main_loop()
