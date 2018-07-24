"""
Entry endpoints for edit,delete,update and get
developed by basweti
"""
# pylint: skip-file
from flask_restplus import Namespace, Resource, fields
from database.db import article

api = Namespace('Diary Entry', description='operations that can be performed on the diary')  # pylint: disable=invalid-name

entry = api.model('Article', {  # pylint: disable=invalid-name
    'id': fields.Integer(required=True, description='article identifier'),
    'title': fields.String(required=True, description='Article Name'),
    'body': fields.String(required=True, description='Article Description'),
    'author': fields.String(required=True, description='Author Name'),
})

Articles = article()  # pylint: disable=invalid-name

parser = api.parser()  # pylint: disable=invalid-name
parser.add_argument('title', type=str, required=True, help='title',
                    location='form')  # pylint: disable=missing-docstring
parser.add_argument('body', required=True, help='description', type=str, location='form')


@api.route('/')
class Entry(Resource):  # pylint: disable=no-self-use
    """
    get the endpoints that don't have Ids at the end
    """

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })# pylint: disable=no-self-use
    def get(self):  # pylint: disable=no-self-use
        """
        return all posts
        :return:
        """
        return Articles

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.expect(entry)
    @api.response(400, 'Validation error')
    @api.marshal_with(entry, code=201, description='Object created') # pylint: disable=no-self-use
    def post(self):
        """
        save a post
        :return:
        """
        Articles.append(api.payload)
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
