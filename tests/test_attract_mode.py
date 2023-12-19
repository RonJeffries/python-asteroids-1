from invaders.raycaster import Raycaster, EmptyCastResult


class TestAttractMode:
    def test_hookup(self):
        assert 2+2 == 4

    def test_raycaster_exists(self):
        Raycaster()

    def test_empty_scan(self):
        caster = Raycaster()
        x = 15
        result = caster.cast(x)
        assert isinstance(result, EmptyCastResult)
