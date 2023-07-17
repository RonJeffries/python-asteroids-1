from pygame import Vector2


class MutatorTest:
    def __init__(self, vector):
        self.vector = vector

    def mutate(self, adjustment):
        self.vector += adjustment


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
