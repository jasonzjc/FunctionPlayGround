# -------------------------------------------------- #
#  Jeff Zhao
#  11/05/3017
#
#  An example to show how to use the MySQL interface of python
#  Need to install MySQLdb module
#
# -------------------------------------------------- #

hostname = '****'     # fill hostname
username = '****'     # fill user name
password = '****'     # fill password
database = '****'     # fill database

# Simple routine to run a query on a database and print the results:
def doQuery(conn) :
    '''
    Execute SQL query
    '''
    cur = conn.cursor()

    cur.execute("SELECT * FROM booking")

    for hotelNo, guestNo, dateFrom, dateTo, roomNo in cur.fetchall() :
        print hotelNo, guestNo, dateFrom

print "Using MySQLdb..."
import MySQLdb
myConnection = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database)
doQuery(myConnection)
myConnection.close()
