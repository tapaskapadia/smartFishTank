import pymysql
import sys

HOSTNAME = ''
USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'sensorstuff'

connection = None


def get_connection():
    global connection
    if connection is not None:
        return connection
    connection = pymysql.connect(host=HOSTNAME,
                                 user=USERNAME,
                                 passwd=PASSWORD,
                                 db=DB_NAME,
                                 port=3306,
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor)
    connection.autocommit(True)
    return connection
