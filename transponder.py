
class Transponder:
    def __init__(self, key):
        self._key = key

    def ping(self, key, function, *args):
        if key == self._key:
            function(* args)