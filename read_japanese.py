# -*- coding: utf-8 -*-

import nltk
import codecs
import re
import urllib
from tinysegmenter import *

# TODO dupes are being returned
# Function to read all lines into dict
segmenter = TinySegmenter()

def page_read(text_in):
    """ string ('file_name.txt') -> unicode string
    Takes in text file and returns a unicode string
    """
    t = codecs.open(text_in,encoding='UTF-8')
    all=t.read()
    t.close()
    return all

def tokenize(all_read):
    """ list -> dict
    takes in all kanji, tokenizes, returns dict
    """
    kanji = {}
    order = 1
    text = (segmenter.tokenize(all_read))
    for tx in text:
        if re.search(ur'[\u4e00-\u9FFF]',tx) and tx not in kanji.keys(): # if in Kanji range (not hira/kata) and not already in dict
            kanji[tx] = order
            order += 1
    return kanji

def ask(all_found):
    """ dict -> dict
     takes all tokenized kanji and loops through, prompting user to lookup or not
    """
    to_lookup = {}
    for k,v in all_found.iteritems():
        question = ''.join(["Lookup ", k.encode('utf-8'), "?\n"])
        need_lookup = raw_input(question)
        if need_lookup is 'y':
            to_lookup[k] = {'order':v}
    return to_lookup

def look(l):
    """ dict -> dict
    gets a dict and looks up the word, adds the def to the dict
    """
    base = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1ZUP' #lookup
    for k,v in l.iteritems():
        print ''.join(['"',k.encode('utf-8'), '"を検索中',])
        web_k = urllib.quote(k.encode('utf8'))
        params = [base, web_k]
        endpoint = ''.join(params)
        response = urllib.urlopen(endpoint) #lookup
        data = response.read()
        clean = nltk.clean_html(data)
        condensed = condensed_def(clean)
        l[k]['definition'] = condensed
    return l

def condensed_def(definition):
    """string -> string
    removed secondary defs, condenses
    """
    if 'matches were found' in definition:
        definition = 'none'
    else:
        end = definition.find('/(P)/')
        definition = definition[29:end]
    return definition

def write_defs(k,t):
    """ dict, output file name -> none
    Takes dict of words and defs and writes them to a text file
    TODO: still not sorted, is the original search term being captured any more?
    """
    output = open(t, 'w')
    for k,v in k.iteritems():
        output.write(k.encode('utf-8'))
        output.write('/' + v['definition'] )
        output.write('\n')
    output.close()
    print 'お待たせいたしました。'

def demo():
    write_defs(look(ask(tokenize(page_read('./tests/jtext.txt')))), './tests/output.txt')
   #page_read('./tests/jtext.txt')

if __name__ == '__main__':
    demo()