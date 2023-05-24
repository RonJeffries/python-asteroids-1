import itertools


from game import Game


class TestGame:
    def test_game_creation(self):
        game = Game(True)
        assert game

    def test_combinations(self):
        things = [1, 2, 3, 4, 5]
        combinations = itertools.combinations(things, 2)
        count = 0
        for _pair in combinations:
            count += 1
        assert count == 10
