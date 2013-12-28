# -*- coding: utf-8 -*-
__author__ = 'scott'



class Kanji:
    def __init__(self, ji, meaning=''):
        self.ji = ji
        self.meaning = meaning
        self.seen = 0
        self.known = 0

    def set_meaning(self, meaning):
        self.meaning = meaning

    def increment_seen(self, amount):
        self.seen += amount

    def increment_seen_by_one(self):
        self.increment_seen(1)



if __name__ == '__main__':
    a = Kanji('私')
    a.set_meaning('I')
    a.increment_seen(2)
    a.increment_seen_by_one()
    print a.meaning
    print a.seen
    print "a means %s" % a.meaning

