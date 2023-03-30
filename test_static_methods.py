class TestStaticMethods:
    def test_one(self):
        assert AllStatic.static_one(1, 1) == 101

    def test_two(self):
        assert AllStatic.static_two(1, 1) == 202


class AllStatic:
    @staticmethod
    def static_one(x, y):
        return 100 * x + y

    @staticmethod
    def static_two(a, b):
        return AllStatic.static_one(2 * a, 2 * b)
