"""
Entry endpoints for edit,delete,update and get
developed by basweti
"""
# pylint: skip-file
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from database.db import article
from models.entry_model import Dict
import psycopg2
from .user import token_required

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

conn = psycopg2.connect(database="df4keijp3j4gsn", user="cslzrgdwqphsdg", password="1f370b6b19a69f6aab5cb73d09fc1edfc4a7eee53680458d01ed498c777b1932",
                        host="ec2-23-23-242-163.compute-1.amazonaws.com", port="5432")
api = Namespace('Diary Entry',
                description='operations that can be performed on the diary')  # pylint: disable=invalid-name

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}

entry = api.model('Article', {  # pylint: disable=invalid-name
    'id': fields.Integer(required=True, description='article identifier'),
    'title': fields.String(required=True, description='Article Name'),
    'body': fields.String(required=True, description='Article Description'),
    'author': fields.String(required=True, description='Author Name'),
})

Articles = article()  # pylint: disable=invalid-name

parser = reqparse.RequestParser()
parser.add_argument('title', help='This field cannot be blank')
parser.add_argument('body', help='This field cannot be blank')


@api.route('/')
class Entry(Resource):  # pylint: disable=no-self-use
    """
    get the endpoints that don't have Ids at the end
    """

    @token_required
    @api.doc(security='apiKey')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })  # pylint: disable=no-self-use
    def get(current_user, self):  # pylint: disable=no-self-use
        """
        return all posts
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT id, title, body, user_id FROM entries WHERE user_id=%s", [current_user[0]])
        rows = cur.fetchall()
        output = []

        for row in rows:
            entry_data = {'id': row[0], 'title': row[1], 'body': row[2], 'user_id': row[3]}
            output.append(entry_data)

        return {'entries': output}

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @token_required
    @api.response(400, 'Validation error')
    @api.param('title', 'title')
    @api.param('body', 'body')
    @api.doc(security='apiKey')
    def post(current_user, self):
        """
        save a post
        :return:
        """

        data = parser.parse_args()
        title = data['title'],
        body = data['body'],
        user_id = current_user[0]

        cur = conn.cursor()
        cur.execute("INSERT INTO entries (TITLE,BODY,USER_ID) \
        VALUES (%s,%s,%s)", (title, body, user_id));
        conn.commit()
        print("Records created successfully")
        return {'result': 'entry added'}, 201


@api.route('/<int:id>')
class Entry_with_id(Resource):  # pylint: disable=invalid-name
    """
    class return all api endpoints that use ids
    """

    @api.doc(security='apiKey')
    @token_required
    def get(current_user, self, id):  # pylint: disable=no-self-use
        """
        get details of particular entry/post
        """
        cur = conn.cursor()
        cur.execute("SELECT id, title, body, user_id FROM entries WHERE user_id=%s AND id=%s", [current_user[0], id])
        row = cur.fetchone()
        entry_data = {'id': row[0], 'title': row[1], 'body': row[2], 'user_id': row[3]}

        return {'entry': entry_data}

    @api.doc(security='apiKey')
    @token_required
    @api.param('title', 'title')
    @api.param('body', 'body')
    def put(current_user, self,
            id):  # pylint: disable=invalid-name #pylint: disable=no-self-use #pylint: disable=redefined-builtin
        """
        Change entry details
        """
        data = parser.parse_args()
        title = data['title'],
        body = data['body']

        cur = conn.cursor()
        cur.execute("UPDATE entries SET title = %s,body = %s WHERE id = %s AND user_id = %s",
                    [title, body, id, current_user[0]]);
        conn.commit()

        return {'message': 'entry updated'}

    @api.doc(security='apiKey')
    @token_required
    def delete(current_user, self,
               id):  # pylint: disable=no-self-use #pylint: disable=redefined-builtin #pylint: disable=invalid-name
        """
        delete entry
        """
        cur = conn.cursor()
        cur.execute("DELETE from entries where id=%s AND user_id=%s", [id, current_user[0]])
        conn.commit()
        return {'message': 'entry deleted'}
