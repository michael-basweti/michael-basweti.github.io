from functools import wraps
import datetime
import uuid
from models.UserModel import User as users
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# pylint: skip-file
app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

api = Namespace('User', description='operations that can be performed on the user')
conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
                        host="127.0.0.1", port="5432")

user_model = api.model('User', {  # pylint: disable=invalid-name
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='User password'),
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='email'),
})

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank')
parser.add_argument('password', help='This field cannot be blank')
parser.add_argument('name', help='This field cannot be blank')
parser.add_argument('email', help='This field cannot be blank')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'token is missing'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE public_id = %s", [data['public_id']])
            current_user = cur.fetchone()
            print("hello" + current_user[3])
        except:
            return {'message': 'token is invalid'}, 401
        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/registration')
# @api.param('username', 'username')
# @api.param('password', 'password')
# @api.param('email', 'email')
# @api.param('name', 'name')
@api.expect(user_model)
@api.doc('Register')
class UserRegistration(Resource):
    def post(self):
        """
        Register a user
        """
        data = parser.parse_args()
        username = data['username'],
        password = generate_password_hash(data['password'], method='sha256'),
        name = data['name'],
        email = data['email'],
        public_id = str(uuid.uuid4())
        str_username = "".join(username)
        str_name = "".join(name)
        str_email = "".join(email)
        str_password = "".join(password)
        str_username.strip()
        str_name.strip()
        str_password.strip()
        str_email.strip()
        if str_username == "" and str_password == "":
            return {"message": "field cannot be empty" }
            if str_name.strip == "" or str_email.strip == "":
                return {"message": "field cannot be empty" }

        registered = users.register(name=str_name,username=str_username,password=str_password,email=str_email,public_id=public_id)
        return registered



@api.route('/login')
@api.param('username', 'username')
@api.param('password', 'password')
class UserLogin(Resource):
    def post(self):
        """
        user login
        """
        data = parser.parse_args()
        username = data['username'],
        password_candidate = data['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        login_data = cur.fetchone()
        if login_data:

            password = login_data[3]
            print(password)
            public_id = login_data[5]
            print(public_id)
            # compare passwords

            if check_password_hash(password, password_candidate):

                token = jwt.encode(
                    {'public_id': public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    app.config['SECRET_KEY'])

                return token.decode('UTF-8')
            else:
                return {'message': 'wrong password'},401
        else:
            return {'message': 'user does not exist'},401



@api.param('id', 'id')
# @api.param('username', 'username')
# @api.param('password', 'password')
# @api.param('email', 'email')
# @api.param('name', 'name')
@api.expect(user_model)
@api.route('/user/update/<int:id>')
class UpdateResource(Resource):
    def put(self, id):
        """
        update users' details
        """
        data = parser.parse_args()
        username = data['username'],
        password = generate_password_hash(data['password'], method='sha256'),
        name = data['name'],
        email = data['email'],

        str_username = "".join(username)
        str_name = "".join(name)
        str_email = "".join(email)
        str_password = "".join(password)
        str_username.strip()
        str_name.strip()
        str_password.strip()
        str_email.strip()
        if str_username == "" or str_password == "" :
            return {"message": "field cannot be empty" }
            if str_name == "" or str_email == "":
                 return {"message": "field cannot be empty" }

        update_users = users.update_user(name=str_name,username=str_username,password=str_password,email=str_email, id=id)
        return update_users


@api.route('/users')
class AllUsers(Resource):
    def get(self):
        """
        Get all users
        """
        all_users = users.get_all_users()
        return all_users





@api.param('id', 'id')
@api.route('/users/<id>')
class GetOneResource(Resource):
    def get(self, id):
        """
        Get one user according to id given
        """
        one_user= users.get_one(id=id)
        return one_user
