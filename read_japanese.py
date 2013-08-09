# -*- coding: utf-8 -*-

import nltk
import codecs
import re
import urllib
from tinysegmenter import *

# Function to read all lines into dict
segmenter = TinySegmenter()

#for each list item, look up meaning
def kanji_define(k):
    """ string -> string
    gets a definition from a string (kanji)
    """
    base = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1ZUP' #lookup
    web_k = urllib.quote(k.encode('utf8'))
    params = [base, web_k]
    endpoint = ''.join(params)
    response = urllib.urlopen(endpoint) #lookup
    data = response.read()
    clean = nltk.clean_html(data)
    return clean

def page_read(text_in):
    """ string ('file_name.txt') -> dict
    Takes utf8 text file and parses kanji, loops through, defines,
    adds to dict
    """
    kanji = {}
    t = codecs.open(text_in,encoding='UTF-8')
    all=t.readlines()
    order = 1
    for line in all:
        text = (segmenter.tokenize(line))
        for tx in text:
            if re.search(ur'[\u4e00-\u9FFF]',tx) and tx not in kanji.keys():
                question = ''.join(["Lookup ", tx.encode('utf-8'), "?\n"])
                lookup = raw_input(question)
                if lookup is 'y':
                    print ''.join(['"',tx.encode('utf-8'), '"を検索中',])
                    kanji[tx] = [kanji_define(tx), order]
                    order += 1
    t.close()
    print ''
    print 'お待たせいたしました。'
    return kanji

def write_defs(k,t):
    """ dict, output file name -> none
    Takes dict of words and defs and writes them to a text file
    """
    output = open(t, 'w')
    #for key, value in k.iteritems():
    for key, value in sorted(k.iteritems(), key=lambda (k,v): (v,k)):
        end = value[0].find('/(P)/')
        if 'matches were found' in value[0]:
            definition = 'none'
        else:
            definition = value[0][29:end]
        output.write(key.encode('utf-8'))
        output.write('/' + definition )
        output.write('\n')
    output.close()

def demo():
    write_defs(page_read('./tests/jtext.txt'), '../test.txt')

if __name__ == '__main__':
    demo()
