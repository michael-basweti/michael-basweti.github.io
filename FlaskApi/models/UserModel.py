import psycopg2
from flask import Flask, request

from flask_restplus import Namespace, Resource, fields, reqparse

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
                        host="127.0.0.1", port="5432")


class User():
    @staticmethod
    def register(name,email,password,public_id,username):
        cur = conn.cursor()
        cur.execute("INSERT INTO users (NAME,EMAIL,PASSWORD,USERNAME,PUBLIC_ID) \
        VALUES (%s,%s,%s,%s,%s )", (name, email, password, username, public_id));
        conn.commit()
        print("Records created successfully")

        return {'message': 'user created'}

    @staticmethod
    def update_user(username, email, name, password, id):
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = %s,email = %s,name = %s,password = %s WHERE id = %s",
                    (username, email, name, password, id))
        conn.commit()

        return {'message': 'user updated'}

    @staticmethod
    def get_all_users():
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id from users")
        rows = cur.fetchall()
        output = []

        for row in rows:
            user_data = {'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'username': row[4],
                         'public_id': row[5]}
            output.append(user_data)

        return {'users': output}

    @staticmethod
    def get_one(id):
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id from users WHERE id = %s", id)
        row = cur.fetchone()

        user_data = {'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'username': row[4],
                     'public_id': row[5]}

        return {'user': user_data}

    # @staticmethod
    # def delete_user(current_user):
    #     cur = conn.cursor()
    #     cur.execute("DELETE from users where id=%s", current_user[0])
    #     conn.commit()
    #     return {'message': 'user deleted'}

