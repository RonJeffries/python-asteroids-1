import pytest
from pygame import Vector2
import time

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

    def test_print(self):
        strs = ["abc", "def", "ghi"]
        joined = ",".join(strs)
        assert joined == "abc,def,ghi"

        vec = (1, 2, 3)
        list_result = [f"{c:.2f}" for c in vec]
        assert list_result == ["1.00", "2.00", "3.00"]

        format_one = f",".join(["1.00", "2.00", "3.00"])
        assert format_one == "1.00,2.00,3.00"

        vertices = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        output = ""
        for v in vertices:
            output += "<" + f",".join(f"{c:.2f}" for c in v) + ">\n"
        assert output == "<1.00,2.00,3.00>\n<4.00,5.00,6.00>\n<7.00,8.00,9.00>\n"

        vectors = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        output = ""
        for vec in vectors:
            output += "<"
            joined_vector = f",".join(f"{c:.2f}" for c in vec)
            output += joined_vector
            output += ">\n"
        assert output == "<1.00,2.00,3.00>\n<4.00,5.00,6.00>\n<7.00,8.00,9.00>\n"

        vectors = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        output = ""
        for vec in vectors:
            output += "<"
            output += f"{vec[0]:.2f},"
            output += f"{vec[1]:.2f},"
            output += f"{vec[2]:.2f}"
            output += ">\n"
        assert output == "<1.00,2.00,3.00>\n<4.00,5.00,6.00>\n<7.00,8.00,9.00>\n"

    def test_odds(self):
        vectors = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15)]
        odds = [vectors[i] for i in range(0, len(vectors), 2)]
        assert odds == [(1, 2, 3), (7, 8, 9), (13, 14, 15)]

    def test_sl_formatting(self):
        def sl_2co(num):
            return f"{num:.2f}"

        assert sl_2co(1.2345) == "1.23"
        assert sl_2co(1.5678) == "1.57"  # rounding

        vec = [1.23, 2.23, 3.23]
        sequence_of_strings = [sl_2co(coord) for coord in vec]
        assert sequence_of_strings == ["1.23", "2.23", "3.23"]
        one_string_with_commas = ",".join(sequence_of_strings)
        assert one_string_with_commas == "1.23,2.23,3.23"

    def test_both_functions(self):
        def sl_2co(num):
            return f"{num:.2f}"

        def sl_v_to_s(vec):
            sequence_of_strings = [sl_2co(coord) for coord in vec]
            one_string_with_commas = ",".join(sequence_of_strings)
            return "<" + one_string_with_commas + ">"

        assert sl_v_to_s((1.2345, 2.2345, 3.2345)) == "<1.23,2.23,3.23>"

    def test_compact_functions(self):
        def sl_v_to_s(vec):
            # used inline three times
            return "<" + ",".join([f"{coord :.2f}" for coord in vec]) + ">"

        assert sl_v_to_s((1.2345, 2.2345, 3.2345)) == "<1.23,2.23,3.23>"

    def test_selecting(self):
        vectors = [(3*a+1, 3*a+2, 3*a+3) for a in range(0, 11)]
        assert len(vectors) == 11
        assert vectors[0:2] == [(1, 2, 3), (4, 5, 6)]
        assert vectors[9:] == [(28, 29, 30), (31, 32, 33)]

        zero = 0
        odds = [vectors[i] for i in range(zero, len(vectors), 2)]
        assert len(odds) == 6
        assert odds[5] == (31, 32, 33)

        one = 1
        evens = [vectors[i] for i in range(one, len(vectors), 2)]  # start at 1!
        assert len(evens) == 5
        assert evens[4] == (28, 29, 30)

    def test_groups(self):
        vectors = [(3*a+1, 3*a+2, 3*a+3) for a in range(0, 8)]  # even number
        pairs = [(vectors[i], vectors[i+1]) for i in range(0, len(vectors), 2)]
        assert pairs[0] == ((1, 2, 3), (4, 5, 6))
        assert pairs[1] == ((7, 8, 9), (10, 11, 12))
        assert pairs[2] == ((13, 14, 15), (16, 17, 18))
        assert pairs[3] == ((19, 20, 21), (22, 23, 24))

    def test_group_up_to_four(self):
        vectors = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        quads = []
        start = 0
        while start < len(vectors):
            chunk = vectors[start:start+4]
            quads.append(chunk)
            start += 4
        assert quads == [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11)]

    def test_sl_group_by(self):
        def sl_2co(num):
            return f"{num:.2f}"

        def sl_v_to_s(vec):
            sequence_of_strings = [sl_2co(coord) for coord in vec]
            one_string_with_commas = ",".join(sequence_of_strings)
            return "<" + one_string_with_commas + ">"

        def sl_group_by(vecs, size):
            grouped = []
            start = 0
            while start < len(vecs):
                chunk = (vecs[start:start+size])
                grouped.append(chunk)
                start += size
            return grouped

        vectors = [(a+0, a+1, a+2) for a in range(0, 99, 3)]
        assert len(vectors) == 33
        formatted = [sl_v_to_s(vec) for vec in vectors]
        assert formatted[0] == "<0.00,1.00,2.00>"
        grouped = sl_group_by(formatted, 4)
        assert grouped[0] == ['<0.00,1.00,2.00>', '<3.00,4.00,5.00>', '<6.00,7.00,8.00>', '<9.00,10.00,11.00>']
        assert grouped[-1] == ['<96.00,97.00,98.00>']
        one_line_each = [", ".join(vec) for vec in grouped]
        assert one_line_each[0] == "<0.00,1.00,2.00>, <3.00,4.00,5.00>, <6.00,7.00,8.00>, <9.00,10.00,11.00>"
        all_lines_packed_by_4 = "\n,".join(line for line in one_line_each)
        print(all_lines_packed_by_4)
        expected = """<0.00,1.00,2.00>, <3.00,4.00,5.00>, <6.00,7.00,8.00>, <9.00,10.00,11.00>
,<12.00,13.00,14.00>, <15.00,16.00,17.00>, <18.00,19.00,20.00>, <21.00,22.00,23.00>
,<24.00,25.00,26.00>, <27.00,28.00,29.00>, <30.00,31.00,32.00>, <33.00,34.00,35.00>
,<36.00,37.00,38.00>, <39.00,40.00,41.00>, <42.00,43.00,44.00>, <45.00,46.00,47.00>
,<48.00,49.00,50.00>, <51.00,52.00,53.00>, <54.00,55.00,56.00>, <57.00,58.00,59.00>
,<60.00,61.00,62.00>, <63.00,64.00,65.00>, <66.00,67.00,68.00>, <69.00,70.00,71.00>
,<72.00,73.00,74.00>, <75.00,76.00,77.00>, <78.00,79.00,80.00>, <81.00,82.00,83.00>
,<84.00,85.00,86.00>, <87.00,88.00,89.00>, <90.00,91.00,92.00>, <93.00,94.00,95.00>
,<96.00,97.00,98.00>"""
        assert all_lines_packed_by_4 == expected

    @pytest.mark.skip("why waste time")
    def test_lookup(self):
        class Something:
            def __init__(self):
                self.value = 0

        something = Something()
        n = 1000000
        t0 = time.time()
        for i in range(n):
            pass
        t1 = time.time()
        for i in range(n):
            something.value
        t2 = time.time()
        for i in range(n):
            x = something.value
        t3 = time.time()
        easy = t1 - t0
        medium = t2 - t1
        hard = t3 - t2
        print(easy, medium, hard)
        assert False

    def test_not_conditional(self):
        low = 1
        high = 10
        too_low = 0
        too_high = 11
        just_right = 5
        assert low < just_right < high
        assert not low < too_low < high
        assert not low < too_high < high








