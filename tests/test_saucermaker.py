import u
from fleets import Fleets
from interactor import Interactor
from saucermaker import SaucerMaker
from test_interactions import FI


class TestSaucerMaker:
    def test_exists(self):
        SaucerMaker()

    def test_creates_saucer(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(SaucerMaker())
        interactor = Interactor(fleets)
        assert not fi.saucers
        interactor.perform_interactions()
        fleets.tick(u.SAUCER_EMERGENCE_TIME)
        assert fi.saucers

    def test_does_not_create_too_many(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.append(SaucerMaker())
        interactor = Interactor(fleets)
        assert not fi.saucers
        interactor.perform_interactions()
        fleets.tick(u.SAUCER_EMERGENCE_TIME)
        assert len(fi.saucers) == 1
        interactor.perform_interactions()
        fleets.tick(u.SAUCER_EMERGENCE_TIME/2)
        assert len(fi.saucers) == 1

