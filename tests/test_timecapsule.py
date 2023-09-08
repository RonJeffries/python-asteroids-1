from timecapsule import TimeCapsule


class TestTimeCapsule:
    def test_can_create(self):
        thing = "thing"
        capsule = TimeCapsule(thing, 2)
