# -*- coding: utf-8 -*-

import codecs
import re
import urllib
from time import sleep

import MySQLdb
import mysql.connector
from mysql.connector import errorcode

import nltk
from database_connect import uname,pw,host,db
from tinysegmenter import *

cnx = mysql.connector.connect(user=uname, password=pw, host=host, database=db)
cursor = cnx.cursor()

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
    lookup_count = len(all_found.keys())
    print "Processing."
    sleep(.5)
    print "Enter y/n to build list of kanji to look up."

    for k, v in all_found.iteritems():
        print "%s kanji remaining" % lookup_count
        if k in known:
            print 'Known kanji: %s. Skipping.' % k
            sleep(.5)
        else:
            question = "Lookup %s?\n" % k.encode('utf-8')
            need_lookup = raw_input(question)
            if need_lookup is 'y':
                to_lookup[k] = {'order':v}
            elif need_lookup is 'n':
                new_known.append(k)
                add_known(new_known)
                print "Added to known database"
        lookup_count -= 1
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

def add_known(known_ji):
    """
    list->none
    Takes the list of known kanji and inserts into database.
    """
    try:
        for ji in known_ji:
            add_ji_query = "INSERT INTO known (ji) VALUES ('%s')" % ji
            cursor.execute(add_ji_query)
            cnx.commit()
    except:
        print "Error: unable to add data"
        cursor.close()
        cnx.close()


def get_known():
    """
    list->none
    Gets known Kanji from database.
    """
    k = []
    ji_count = 0
    query = "SELECT ji FROM known"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for (c) in result:
            k.append(c[0])
            ji_count += 1
    except:
        print "Error: unable to fetch data"
        cursor.close()
        cnx.close()

    return k


def demo():
    write_defs(look(ask(tokenize(page_read('./tests/jtext.txt')))), './tests/output.txt')

if __name__ == '__main__':
    demo()
