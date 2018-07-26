import psycopg2

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
host="127.0.0.1", port="5432")
print ("Opened database successfully")
cur = conn.cursor()
cur.execute('''CREATE TABLE users
(ID SERIAL PRIMARY KEY NOT NULL,
NAME VARCHAR NOT NULL,
EMAIL VARCHAR NOT NULL,
PASSWORD VARCHAR NOT NULL,
USERNAME VARCHAR NOT NULL,
PUBLIC_ID VARCHAR NOT NULL);''')
print ("Table created successfully")
conn.commit()
conn.close()