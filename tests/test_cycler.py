from cycler import Cycler


class TestCycler:
    def test_exists(self):
        Cycler([])

    def test_cycles(self):
        values = [0, 100, 200]
        cycler = Cycler(values)
        for i in range(6):
            expected = (i % len(values)) * 100
            checked = cycler.next()
            assert checked == expected