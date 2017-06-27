import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "football64",
                           db = "Football",
                           charset='utf8')
    c = conn.cursor()

    return c, conn
