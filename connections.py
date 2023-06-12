import psycopg2
from psycopg2.extras import RealDictCursor
import os 

host='localhost'
user='postgres'
database='wifi_connections'
password='Ssebugenyijuma95'
port_id=5432


class DBase:
    # db connection
    def Connect():
        connection = ''
        try:
            connection = psycopg2.connect(
            database=os.getenv('database'), 
            user=os.getenv('user'), 
            host=os.getenv('host'), 
            port= os.getenv('port_id'),
            password=os.getenv("password")
            )
        except psycopg2.Error as e:
            print(e)
        return connection
    
    # db cursor 
    def Cursor(dbconnection):
        cursor = ''
        try:
            cursor = dbconnection.cursor(cursor_factory=RealDictCursor)
        except:
            print("unable to create cursor")
        return cursor
   