import psycopg2

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
host="127.0.0.1", port="5432")
print ("Opened database successfully")
cur = conn.cursor()
cur.execute('''CREATE TABLE entries
(ID SERIAL PRIMARY KEY NOT NULL,
TITLE VARCHAR NOT NULL,
BODY TEXT NOT NULL,
USER_ID VARCHAR NOT NULL);''')
print ("Table created successfully")
conn.commit()
conn.close()