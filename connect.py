# -*- coding: utf-8 -*-

from database_connect import uname,pw,host,db
import MySQLdb
import mysql.connector
from mysql.connector import errorcode


def add_known(known_ji):
    """
    list->none
    Takes the list of known kanji and inserts into database.
    """
    cnx = mysql.connector.connect(user=uname, password=pw, host=host, database=db)
    cursor = cnx.cursor()
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
    cnx = mysql.connector.connect(user=uname, password=pw, host=host, database=db)
    cursor = cnx.cursor()
    k = []
    ji_count = 0
    query = "SELECT ji FROM known"
    try:
        cursor.execute(query)
        for (c) in cursor:
            k.append(c)
            ji_count += 1
    except:
        print "Error: unable to fetch data"
        cursor.close()
        cnx.close()

    return k


def demo():
    add_known(['test10','test13'])
    get_known()

if __name__ == '__main__':
    demo()

