__author__ = 'scott'


class Kanji:
    def __init__(self, ji, meaning, seen, known):
        self.ji = ji
        self.meaning =  meaning
        self.seen = seen
        self.known = known

    def definition(self):
        return self.meaning


