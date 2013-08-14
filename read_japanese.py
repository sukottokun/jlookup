# -*- coding: utf-8 -*-

import nltk
import codecs
import re
import urllib
from tinysegmenter import *

# Function to read all lines into dict
segmenter = TinySegmenter()

def page_read(text_in):
    """ string ('file_name.txt') -> unicode string
    Takes in text file and returns a unicode string
    """
    t = codecs.open(text_in,encoding='UTF-8')
    all_text=t.read()
    t.close()
    return all_text

def tokenize(all_read):
    """ list -> dict
    takes in all kanji, tokenizes, returns dict
    """
    kanji = {}
    order = 1
    text = (segmenter.tokenize(all_read))
    for tx in text:
        # if in Kanji range (not hira/kata) and not already in dict
        if re.search(ur'[\u4e00-\u9FFF]',tx) and tx not in kanji.keys():
            kanji[tx] = order
            order += 1
    return kanji

def get_kanji_i_know():
    """ none _> list
    Loads a list of known words, so user can skip over them when selecting. Eliminates simple words.
    """
    t = codecs.open('./tests/known_kanji.txt',encoding='UTF-8')
    known=t.readlines()
    t.close()
    return known

def write_new_kanji_i_know(kanji):
    """ list -> none
    takes a list of new kanji and adds them to the text file of kanji the user knows.
    """
    output = open('./tests/known_kanji.txt', 'w+')
    for k in kanji:
        output.write(k.encode('utf-8'))
        output.write('\n')
    output.close()

def ask(all_found):
    """ dict -> dict
     takes all tokenized kanji and loops through, prompting user to lookup or not
    """
    known = get_kanji_i_know()
    new_known = []
    to_lookup = {}
    for k,v in all_found.iteritems():
        if k not in known: # TODO not working
            question = ''.join(["Lookup ", k.encode('utf-8'), "?\n"])
            need_lookup = raw_input(question)
            if need_lookup is 'y':
                to_lookup[k] = {'order':v}
            elif need_lookup is 'n':
                new_known.append(k)
    write_new_kanji_i_know(new_known)
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
    """
    output = open(t, 'w')
    for k,v in sorted(k.iteritems(), key=lambda (k,v): v['order']):
        output.write(k.encode('utf-8'))
        output.write('/' + v['definition'] )
        output.write('\n')
    output.close()
    print 'お待たせいたしました。'

def demo():
    write_defs(look(ask(tokenize(page_read('./tests/jtext.txt')))), './tests/output.txt')

if __name__ == '__main__':
    demo()
