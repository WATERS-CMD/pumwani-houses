import psycopg2
from psycopg2.extras import RealDictCursor
import os

connection=None
class Dbase:
  def connection(dbconnection):
      try:
        connection=psycopg2.connect(
          database=os.getenv('trials'),
          user=os.getenv('postgres'),
          password=os.getenv('Ssebugenyijuma95'),
          port_id=os.getenv('5432')
        )
      except psycopg2.Error as e:
        print(e)
      return dbconnection
    

  def cursor(Dbconnection):

    try:
      cursor=Dbconnection.cursor(cursor_factory=RealDictCursor)
    except:
      print("unable to connect cursor")
    return 

   