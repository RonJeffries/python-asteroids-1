class TestStaticMethods:
    def test_one(self):
        assert AllStatic.static_one(1, 1) == 101

    def test_two(self):
        assert AllStatic.static_two(1, 1) == 202

    def test_class_variables(self):
        t = AllStatic()
        assert t.direction == -1
        t.flip()
        assert t.direction == 1
        u = AllStatic()
        assert u.direction == 1
        assert t.direction == 1
        u.flip()
        assert u.direction == -1
        assert t.direction == -1


class AllStatic:
    direction = -1

    @staticmethod
    def static_one(x, y):
        return 100 * x + y

    @staticmethod
    def static_two(a, b):
        return AllStatic.static_one(2 * a, 2 * b)

    @staticmethod
    def flip():
        AllStatic.direction = - AllStatic.direction
