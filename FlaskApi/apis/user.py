from functools import wraps
import datetime
import uuid
import re
from models.UserModel import User as users
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import FileStorage
import jwt
import os
import werkzeug
from werkzeug.utils import secure_filename

# pylint: skip-file
app = Flask(__name__)  # pylint: disable=invalid-name

SECRET=os.getenv('SECRET_KEY')


api = Namespace('User', description='operations that can be performed on the user')
conn = psycopg2.connect(database="mydiary",password="trizabas2017",host="127.0.0.1",port="5432",user="postgres")

user_model = api.model('Register', {  # pylint: disable=invalid-name
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='User password'),
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='email'),
    
})
login_model = api.model('Login', {  # pylint: disable=invalid-name
    'password': fields.String(required=True, description='User password'),
    'email': fields.String(required=True, description='email'),

})

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank')
parser.add_argument('password', help='This field cannot be blank')
parser.add_argument('name', help='This field cannot be blank')
parser.add_argument('email', help='This field cannot be blank')

# file_upload = reqparse.RequestParser()
# file_upload.add_argument('xls_file',  
#                          type=werkzeug.datastructures.FileStorage, 
#                          location='files', 
#                          required=False, 
#                          help='XLS file')

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'token is missing'}, 401

        try:
            data = jwt.decode(token, SECRET)
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
        username = data['username']
        password = data['password']
        hashed_password = generate_password_hash(password, method='sha256')
        name = data['name']
        email = data['email']
        public_id = str(uuid.uuid4())
        now=datetime.datetime.now()
        date= str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        str_username = "".join(username)
        str_name = "".join(name)
        str_email = "".join(email)
        str_password = "".join(password)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s",[str_email])
        if cur.rowcount>0:
            return {"message":"email is already taken"}
        elif len(str_password.strip())<6:
            return {"message":"Password should be 6 characters and above"}
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', str_email):
                return {"message":"email not valid,change format"}
            #all fields should be filled
        elif not all((str_email.strip(),str_name.strip(),str_password.strip(),str_username.strip())):
            return {"message": "No fields should be empty"}
        
        else:
            users.register(name=str_name,username=str_username,password=hashed_password,email=str_email,public_id=public_id,date=date)
            return {"message":"user created"}


@api.route('/login')
#@api.param('email', 'email')
#@api.param('password', 'password')
@api.expect(login_model)
class UserLogin(Resource):
    def post(self):
        """
        user login
        """
        data = parser.parse_args()
        email = data['email'],
        password_candidate = data['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        login_data = cur.fetchone()
        if login_data:

            password = login_data[3]
            print(password)
            public_id = login_data[5]
            print(public_id)
            # compare passwords

            if check_password_hash(password, password_candidate):

                token = jwt.encode(
                    {'public_id': public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=3)},
                    SECRET)

                return {"token":token.decode('UTF-8')}
                
            else:
                return {"message": "wrong password"},401
        else:
            return {"message": "user does not exist"},401




@api.expect(user_model)
@api.route('/user/update/')
class UpdateResource(Resource):
    @api.doc(security='apiKey')
    @token_required
    def put(current_user, self):
        """
        update users' details
        """
        data = parser.parse_args()
        username = data['username']
        password = data['password']
        hashed_password = generate_password_hash(password, method='sha256')
        name = data['name']
        email = data['email']
        str_username = "".join(username)
        print(username)
        print(name)
        print(email)
        str_name="".join(name)
        
        str_email = "".join(email)
        str_password = "".join(password)
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND NOT(id=%s)",[str_email,current_user[0]])
        if cur.rowcount>0:
            return {"message":"email is already taken"}
        elif len(str_password.strip())<6:
            return {"message":"Password should be 6 characters and above"}
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', str_email):
                return {"message":"email not valid,change format"}
            #all fields should be filled
        elif not all((str_email.strip(),str_name.strip(),str_password.strip(),str_username.strip())):
            return {"message": "No fields should be empty"}

        if not all((str_email.strip(),str_password.strip(),str_name.strip(),str_username.strip())):
            return {"message": " No field field cannot be empty" }
        else:

            update_users = users.update_user(name=str_name,username=str_username,password=hashed_password,email=str_email, current_user=current_user)
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


@api.route('/user')
class GetCurrent(Resource):
    @api.doc(security='apiKey')
    @token_required
    def get(current_user, self):
        """
        Get logged in user
        """
        one_user= users.get_current(current_user=current_user)
        return one_user

@api.route('/delete')
class GetCurrent(Resource):
    @api.doc(security='apiKey')
    @token_required
    def delete(current_user, self):
        """
        Delete logged in user
        """
        delete_user= users.delete_user(current_user=current_user)
        return delete_user

# @api.route('/add_photo')
# @api.expect(file_upload)
# class AddPhoto(Resource):
#     @api.doc(security='apiKey')
#     @token_required
#     def post(current_user, self):
#         """
#         Upload user photo
#         """
#         args = file_upload.parse_args()
#         if not args['xls_file']:
#             destination = os.path.join(app.config.get('UPLOAD_FOLDER'), 'medias/')
#             if not os.path.exists(destination):
#                 os.makedirs(destination)
#             xls_file = '%s%s' % (destination, 'custom_file_name.xls')
#             print(xls_file)
#             args['xls_file'].save(xls_file)
        
#         return {'status': 'Done'}