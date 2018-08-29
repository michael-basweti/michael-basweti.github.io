import psycopg2
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
import os



conn = psycopg2.connect(database="mydiary",password="trizabas2017",host="127.0.0.1",port="5432",user="postgres")


class User():
    @staticmethod
    def register(name,email,password,public_id,username,date):
        cur = conn.cursor()
        cur.execute("INSERT INTO users (NAME,EMAIL,PASSWORD,USERNAME,PUBLIC_ID,DATE) \
        VALUES (%s,%s,%s,%s,%s,%s )", (name, email, password, username, public_id,date))
        conn.commit()
        print("Records created successfully")
        


    @staticmethod
    def update_user(username, email, name, password, current_user):
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = %s,email = %s,name = %s,password = %s WHERE id = %s",
                    (username, email, name, password, current_user[0]))
        conn.commit()

        return {'message': 'user updated'}

    @staticmethod
    def get_all_users():
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id,date from users")
        rows = cur.fetchall()
        output = []

        for row in rows:
            user_data = {'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'username': row[4],
                         'public_id': row[5],'date':row[6]}
            output.append(user_data)

        return output

    @staticmethod
    def get_one(id):
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id,date from users WHERE id = %s", id)
        row = cur.fetchone()

        user_data = {'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'username': row[4],
                     'public_id': row[5],'date':row[6]}

        return {'user': user_data}

    @staticmethod
    def delete_user(current_user):
        cur = conn.cursor()
        cur.execute("DELETE from entries where user_id=%s;DELETE from users where id=%s", [current_user[0],current_user[0]])
        conn.commit()
        return {'message': 'user deleted'}


    @staticmethod
    def get_current(current_user):
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM entries WHERE user_id=%s", [current_user[0]])
        entry=cur.fetchone()
        print(entry)
        cur.execute("SELECT id, name, email, password, username,public_id,date from users WHERE id = %s", [current_user[0]])
        row = cur.fetchone()

        user_data = {'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'username': row[4],
                     'public_id': row[5],'date':row[6],'entries':entry}

        return user_data