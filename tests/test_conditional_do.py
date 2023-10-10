

class DoIfTrue:
    def __init__(self, yes_no = True):
        self.yes_no = yes_no

    def do(self, fcn):
        if self.yes_no:
            return fcn()

    def done(self):
        self.yes_no = True


class TestConditionalDo:
    def test_does(self):
        doer = DoIfTrue()
        result = doer.do(lambda: 66)
        assert result == 66

    def test_draw(self):
        doer = DoIfTrue(False)
        drawn = "no"
        drawn = doer.do(lambda: "yes")
        assert drawn == None
        doer.done()
        drawn = doer.do(lambda: "yes")
        assert drawn == "yes"
