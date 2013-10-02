# -*- coding: utf-8 -*-

import nltk
import codecs
import re
import urllib
from connect import *
from tinysegmenter import *
from time import sleep

# Function to read all lines into dict
segmenter = TinySegmenter()


def page_read(text_in):
    """ string ('file_name.txt') -> unicode string
    Takes in text file and returns a unicode string
    """
    t = codecs.open(text_in,encoding='UTF-8')
    all_text=t.read()
    t.close()
    print "File Read."
    sleep(.5)
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


def ask(all_found):
    """ dict -> dict
     takes all tokenized kanji and loops through, prompting user to lookup or not
    """
    known = get_known()
    new_known = []
    to_lookup = {}
    print "Processing."
    sleep(.5)
#TODO not recognizing known kanji

    for k, v in all_found.iteritems():
        if k in known:
            print 'Known kanji: %s. Skipping.' % k
            sleep(.5)
        else:
            question = ''.join(["Lookup ", k.encode('utf-8'), "?\n"])
            need_lookup = raw_input(question)
            if need_lookup is 'y':
                to_lookup[k] = {'order':v}
            elif need_lookup is 'n':
                new_known.append(k)
    add_known(new_known)
    return to_lookup


def look(l):
    """ dict -> dict
    gets a dict and looks up the word, adds the def to the dict
    """
    base = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1ZUP' #lookup
    print "Beginning search..."
    sleep(.5)
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
    print "Writing."
    sleep(.5)
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
