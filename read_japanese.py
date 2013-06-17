# -*- coding: utf-8 -*-

import os
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import codecs
import sys
import re
import requests
import urllib
import pprint
from tinysegmenter import *

''' Function to read all lines into dict'''
segmenter = TinySegmenter() #read

#for each list item, look up meaning
def kanji_define(k):
    ''' string -> string
    gets a definition from a string (kanji)
    '''
    base = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1ZUP' #lookup
    web_k = urllib.quote(k.encode('utf8'))
    params = [base, web_k]
    endpoint = ''.join(params)
    response = urllib.urlopen(endpoint) #lookup
    data = response.read()
    clean = nltk.clean_html(data)
    return clean

def page_read(text_in):
    ''' string ('file_name.txt') -> dict
    Takes utf8 text file and parses kanji, loops through, defines,
    adds to dict
    '''
    kanji = {}
    t = codecs.open(text_in,encoding='UTF-8')
    all=t.readlines()

    for line in all:
        text = (segmenter.tokenize(line))
        for tx in text:
            if re.search(ur'[\u4e00-\u9FFF]',tx):
                kanji[tx] = kanji_define(tx)

    t.close()
    return kanji

def write_defs(k,t):
    ''' dict -> none
    Takes dict of words and defs and writes them to a text file
    '''
    output = open(t, 'w')
    for key, value in k.iteritems():
        end = value.find('/(P)/')
        if 'matches were found' in value:
            definition = 'none'
        else:
            definition = value[29:end]
        output.write(key.encode('utf-8'))
        output.write('\n')
        output.write(definition)
        output.write('\n\n')
    output.close()

def demo():
    write_defs(page_read('./tests/sensei.txt'), '../test.txt')

if __name__ == '__main__':
    demo()
