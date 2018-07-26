"""
Entry endpoints for edit,delete,update and get
developed by basweti
"""
# pylint: skip-file
from flask import Flask,request
from flask_restplus import Namespace, Resource, fields, reqparse
from database.db import article
from models.entry_model import Dict
import psycopg2
from .user import token_required


app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
host="127.0.0.1", port="5432")
api = Namespace('Diary Entry', description='operations that can be performed on the diary')  # pylint: disable=invalid-name

authorizations ={
    'apiKey':{
        'type':'apiKey',
        'in':'header',
        'name':'x-access-token'
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
parser.add_argument('title', help = 'This field cannot be blank')
parser.add_argument('body', help = 'This field cannot be blank')

@api.route('/')

class Entry(Resource):  # pylint: disable=no-self-use
    """
    get the endpoints that don't have Ids at the end
    """
    @token_required
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })# pylint: disable=no-self-use
    
    def get(self,current_user):  # pylint: disable=no-self-use
        """
        return all posts
        :return:
        """
        return Articles

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })

    @token_required
    @api.response(400, 'Validation error')
    @api.param('title', 'title')
    @api.param('body', 'body')
    @api.doc(security='apiKey')
    def post(self,current_user):
        """
        save a post
        :return:
        """
        data = parser.parse_args()
        title = data['title'],
        body =data['body'],
        user_id = current_user[0]
        

        cur = conn.cursor()
        cur.execute("INSERT INTO entries (TITLE,BODY,USER_ID) \
        VALUES (%s,%s,%s)",(title,body,user_id));
        conn.commit()
        print ("Records created successfully")
        return {'result': 'language added'}, 201


@api.route('/<int:id>')
class Entry_with_id(Resource):  # pylint: disable=invalid-name
    """
    class return all api endpoints that use ids
    """

    def get(self, id):  # pylint: disable=no-self-use
        """
        get details of particular entry/post
        """
        result = [article for article in Articles if article['id'] == id]
        return result

    @api.doc(parser=parser)
    def put(self, id):  # pylint: disable=invalid-name #pylint: disable=no-self-use #pylint: disable=redefined-builtin
        """
        Change entry details
        """
        args = parser.parse_args()
        for index, article in enumerate(Articles):  # pylint: disable=redefined-outer-name
            if article['id'] == id:  # pylint: disable=invalid-name
                Articles[index]['title'] = args['title']
                Articles[index]['body'] = args['body']
                return article, 201
        return None, 201

    def delete(self,
               id):  # pylint: disable=no-self-use #pylint: disable=redefined-builtin #pylint: disable=invalid-name
        """
        delete entry
        """
        for index, article in enumerate(Articles):  # pylint: disable=redefined-outer-name
            if article['id'] == id:
                del Articles[index]
                return {"response": "Entry deleted"}, 204
        return None, 404
