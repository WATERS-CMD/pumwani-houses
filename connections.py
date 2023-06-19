import psycopg2

hostname='localhost'
database='pumwani'
user='postgres'
password='12345'
port_id=5432

conn=None
cur=None

try:
    conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)

    cur=conn.cursor()
    create_script='''CREATE TABLE IF NOT EXISTS users(
                        id serial PRIMARY KEY,
                        firstname varchar(20) NOT NULL,
                        lastname varchar(20) NOT NULL,
                        housenumber varchar(10) NOT NULL UNIQUE,
                        telephone varchar(14) NOT NULL,
                        email varchar (60) NOT NULL UNIQUE,
                        password varchar(60) NOT NULL)'''
    cur.execute(create_script)

    insert_script='INSERT INTO users(id, firstname,lastname,housenumber,telephone,email,password) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    insert_values=[]
    for record in insert_values:
        cur.execute(insert_script, record)

    cur.execute('SELECT * FROM users')
    for records in cur.fetchall():
        print(records[0],records[1])

    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()