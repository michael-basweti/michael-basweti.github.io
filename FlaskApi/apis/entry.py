"""
Entry endpoints for edit,delete,update and get
developed by basweti
"""
# pylint: skip-file
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from database.db import article
from models.UserEntry import EntryModel as entries
import psycopg2
from .user import token_required

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
                        host="127.0.0.1", port="5432")
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
        all_entries = entries.get_all(current_user=current_user)
        return all_entries

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

        post_entry = entries.post_entry(body=body,title = title,user_id=user_id)

        return post_entry


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
        get_single = entries.get_one_entry(current_user=current_user,id=id)
        return get_single

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

        edit = entries.edit_entry(id=id,title=title,body=body,current_user=current_user)
        return edit

    @api.doc(security='apiKey')
    @token_required
    def delete(current_user, self,
               id):  # pylint: disable=no-self-use #pylint: disable=redefined-builtin #pylint: disable=invalid-name
        """
        delete entry
        """
        delete_entry = entries.delete_entry(id=id,current_user=current_user)
        return delete_entry
