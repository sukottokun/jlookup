# -*- coding: utf-8 -*-
__author__ = 'scott'



class Kanji:
    def __init__(self, ji, meaning=''):
        self._ji = ji
        self._meaning = meaning
        self._seen = 0
        self._known = 0
        print "Kanji object is created."


    def increment_seen(self, amount):
        self._seen += amount

    def increment_seen_by_one(self):
        self.increment_seen(1)

    def __repr__(self):
        return self._ji

    def __str__(self):
        return "An instance of class Test with state: a=%s" % self._ji



if __name__ == '__main__':
    a = Kanji('猫')
    a.meaning = "I, Myself"
    a.increment_seen(2)
    a.increment_seen_by_one()
    print a._meaning
    print a._seen
    print "a means %s" % a._meaning
    print a

