# Asteroids Main program
from core.game import Game

asteroids_game: Game

if __name__ == "__main__":
    asteroids_game = Game()
    asteroids_game.main_loop()
