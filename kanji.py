# -*- coding: utf-8 -*-
__author__ = 'scott'



class Kanji:
    def __init__(self, ji, meaning=''):
        self.ji = ji
        self.meaning = meaning
        self.seen = 0
        self.known = 0
        print "Kanji object is created."


    def increment_seen(self, amount):
        self.seen += amount

    def increment_seen_by_one(self):
        self.increment_seen(1)

    def __repr__(self):
        return self.ji

    def __str__(self):
        return self.ji



if __name__ == '__main__':
    a = Kanji('猫')
    a.meaning = "I, Myself"
    a.increment_seen(2)
    a.increment_seen_by_one()
    print("{0} means {1}, and has been seen {2} times".format(a, a.meaning, a.seen))

