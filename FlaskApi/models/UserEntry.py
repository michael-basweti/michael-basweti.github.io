import psycopg2
from flask import Flask, request
from apis.user import token_required
from flask_restplus import Namespace, Resource, fields, reqparse

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
                        host="127.0.0.1", port="5432")




class EntryModel():

    @staticmethod
    def get_all(current_user):
        cur = conn.cursor()
        cur.execute("SELECT id, title, body, user_id FROM entries WHERE user_id=%s", [current_user[0]])
        rows = cur.fetchall()
        output = []

        for row in rows:
            entry_data = {'id': row[0], 'title': row[1], 'body': row[2], 'user_id': row[3]}
            output.append(entry_data)

        return {'entries': output}

    @staticmethod
    def post_entry(title,body,user_id):
        cur = conn.cursor()
        cur.execute("INSERT INTO entries (TITLE,BODY,USER_ID) \
        VALUES (%s,%s,%s)", (title, body, user_id))
        conn.commit()
        print("Records created successfully")
        return {'result': 'entry added'}, 201
    @staticmethod
    def get_one_entry(current_user,id):
        cur = conn.cursor()
        cur.execute("SELECT id, title, body, user_id FROM entries WHERE user_id=%s AND id=%s", [current_user[0], id])
        row = cur.fetchone()
        entry_data = {'id': row[0], 'title': row[1], 'body': row[2], 'user_id': row[3]}

        return {'entry': entry_data}

    @staticmethod
    def edit_entry(title,body,id,current_user):
        cur = conn.cursor()
        cur.execute("UPDATE entries SET title = %s,body = %s WHERE id = %s AND user_id = %s",
                    [title, body, id, current_user[0]])
        conn.commit()

        return {'message': 'entry updated'}
    @staticmethod
    def delete_entry(current_user,id):
        cur = conn.cursor()
        cur.execute("DELETE from entries where id=%s AND user_id=%s", [id, current_user[0]])
        conn.commit()
        return {'message': 'entry deleted'}



