from pygame import Vector2


class MutatorTest:
    def __init__(self, vector):
        self.vector = vector

    def mutate(self, adjustment):
        self.vector += adjustment


class MonkeyVictim:
    def ignore_list(self, *names):
        for name in names:
            self.safe_ignore(name)

    def safe_ignore(self,name):
        try:
            getattr(self, name)
        except AttributeError:
            self.ignore(name)

    def ignore(self, name):
        setattr(self, name, self.nothing)

    def nothing(self):
        pass

    def three(self):
        return 3

    def four(self):
        return 4


class TestPython:
    def test_vectors_mutate(self):
        v1 = Vector2(1, 2)
        v1_original = v1
        assert v1 is v1_original
        v2 = Vector2(3, 4)
        v1 += v2
        assert v1 is v1_original
        v1 = v1 + v2
        assert v1 is not v1_original

    def test_empty_string(self):
        assert not ""
        assert "False"

    def test_show_vector_aliasing(self):
        original = Vector2(100, 100)
        copied = original
        copied += Vector2(10, 20)
        assert copied == Vector2(110, 120)
        assert original == copied  # !!! aliasing.

    def test_aliasing_of_parameters(self):
        original = Vector2(100, 100)
        mutator = MutatorTest(original)
        mutator.mutate(Vector2(10, 20))
        assert mutator.vector == Vector2(110, 120)
        assert original == mutator.vector  # aliasing!!!

    def test_aliasing_of_int(self):
        original = 15
        mutator = MutatorTest(original)
        mutator.mutate(5)
        assert mutator.vector == 20
        assert original == 15

    def test_aliasing_of_list(self):
        original = [1, 2, 3]
        mutator = MutatorTest(original)
        mutator.mutate("a")
        assert mutator.vector == [1, 2, 3, "a"]
        assert original == mutator.vector  # aliasing!!

    def test_simple_monkey(self):
        m = MonkeyVictim()
        assert m.four() == 4
        setattr(m, "four", m.nothing)
        assert not m.four()

    def test_monkey_independent(self):
        m1 = MonkeyVictim()
        m2 = MonkeyVictim()
        setattr(m1, "four", m1.nothing)
        assert not m1.four()
        assert m2.four() == 4

    def test_ignore_method(self):
        m = MonkeyVictim()
        assert m.four() == 4
        m.ignore("four")
        assert not m.four()

    def test_safe_ignore(self):
        m = MonkeyVictim()
        assert m.four() == 4
        m.safe_ignore("four")
        assert m.four() == 4

    def test_safe_list(self):
        m = MonkeyVictim()
        m.ignore_list("four", "six")
        assert m.four() == 4
        assert not m.six()

