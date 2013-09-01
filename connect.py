from database_connect import cnx

cursor = cnx.cursor()

def add_employee():
    data_employee = 51011
    add_employee = "INSERT INTO t (c) VALUES (%d)" % data_employee

    # Insert new employee
    cursor.execute(add_employee)

    # Make sure data is committed to the database
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
http://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
import MySQLdb
db = MySQLdb.connect(host="localhost", user="stackoverflow", passwd="", db="stackoverflow")
cursor = db.cursor()
try:
    sql = 'create table if not exists anzahlids( tweetid int ) ; '
except:
    #ignore
    pass

sql = ("""INSERT INTO anzahlids (tweetid) VALUES (%s)""")
data = [1,2,3,4,5,6,7,8,9]
length = [len(data)]
cursor.executemany(sql,length)
db.commit()
'''
