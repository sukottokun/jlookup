from database_connect import cnx

"""
http://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
http://dev.mysql.com/doc/connector-python/en/connector-python-reference.html
"""

cursor = cnx.cursor()

def add_known(known_ji):
    """
    list->none
    Takes the list of known kanji and inserts into database.
    """
    add_ji_query = "INSERT INTO known (ji) VALUES (%s)" % known_ji
    for ji in known_ji:
        cursor.execute(add_ji_query, ji)

    cnx.commit()
    cursor.close()
    cnx.close()

def get_employee():
    query = "SELECT c FROM t "
    cursor.execute(query)
    for (c) in cursor:
        print("{} is not a number".format(c))
    cursor.close()
    cnx.close()

def demo():
    get_employee()

if __name__ == '__main__':
    demo()


'''
'''
