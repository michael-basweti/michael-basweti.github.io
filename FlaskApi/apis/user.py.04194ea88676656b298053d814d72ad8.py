from flask import Flask,request
from flask_restplus import Namespace, Resource, fields, reqparse
import psycopg2
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
import datetime
from functools import wraps


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
parser.add_argument('username', help = 'This field cannot be blank')
parser.add_argument('password', help = 'This field cannot be blank')
parser.add_argument('name', help = 'This field cannot be blank')
parser.add_argument('email', help = 'This field cannot be blank')

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message':'token is missing'},401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            cur = conn.cursor()
            current_user =  cur.execute("SELECT * FROM users WHERE public_id = %s",data)
            cur.fetchone()
        except:
            return {'message':'token is invalid'},401
        return f(current_user,*args,**kwargs)
    return decorated

@api.route('/registration')
@api.param('username', 'username')
@api.param('password', 'password')
@api.param('email', 'email')
@api.param('name', 'name')
@api.doc('Register')
class UserRegistration(Resource):
    def post(self):
        """
        Register a user
        """
        data = parser.parse_args()
        username = data['username'],
        password =generate_password_hash(data['password'], method='sha256'),
        name = data['name'],
        email = data['email'],
        public_id = str(uuid.uuid4())

        cur = conn.cursor()
        cur.execute("INSERT INTO users (NAME,EMAIL,PASSWORD,USERNAME,PUBLIC_ID) \
        VALUES (%s,%s,%s,%s,%s )",(name,email,password,username,public_id));
        conn.commit()
        print ("Records created successfully")
        
        return {'message':'user created'}

@api.route('/login')
@api.param('username', 'username')
@api.param('password', 'password')
class UserLogin(Resource):
    def post(self):
        
        data = parser.parse_args()
        username = data['username'],
        password_candidate =data['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        login_data = cur.fetchone()
        if login_data:
            
            password = login_data[3]
            print(password)
            public_id = login_data[5]
            #compare passwords

            if check_password_hash(password,password_candidate):
                
                token = jwt.encode({'public_id':public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)},app.config['SECRET_KEY'])
                return {'token':token.decode('UTF-8')}
            else:
                return {'message':'wrong password'}
        else:
            return {'message':'user does not exist'}

        
      
@api.route('/logout/access')
class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
@api.route('/logout/refresh')      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


@api.param('id', 'id')
@api.param('username', 'username')
@api.param('password', 'password')
@api.param('email', 'email')
@api.param('name', 'name')      
@api.route('/user/update/<int:id>')      
class TokenRefresh(Resource):
    def put(self,id):
        """
        update users' details
        """
        data = parser.parse_args()
        username = data['username'],
        password =generate_password_hash(data['password'], method='sha256'),
        name = data['name'],
        email = data['email'],
        

        cur = conn.cursor()
        cur.execute("UPDATE users SET username = %s,email = %s,name = %s,password = %s WHERE id = %s", (username,email,name,password,id));
        conn.commit()
        
        return {'message': 'user updated'}
      
@api.route('/users')      
class AllUsers(Resource):
    def get(self):
        """
        Get all users
        """
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id from users")
        rows = cur.fetchall()
        output = []
        
        for row in rows:
            user_data = {}
            user_data['id'] = row[0]
            user_data['name'] = row[1]
            user_data['email'] = row[2]
            user_data['password'] = row[3]
            user_data['username'] = row[4]
            user_data['public_id'] = row[5]
            output.append(user_data)

        return {'users': output}

@api.route('/delete/<id>')   
@api.param('id', 'id')
class DeleteResource(Resource):
    @token_required
    @api.doc(security='apiKey')
    def delete(self,current_user,id):
        """
        delete a specific user
        """
        cur = conn.cursor()
        cur.execute("DELETE from users where id=%s",id)
        conn.commit()
        return {'message': 'user deleted'}

@api.param('id', 'id')
@api.route('/users/<id>')      
class SecretResource(Resource):
    def get(self,id):
        """
        Get one user according to id given
        """
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, username,public_id from users WHERE id = %s", id)
        row = cur.fetchone()

        user_data = {}
        user_data['id'] = row[0]
        user_data['name'] = row[1]
        user_data['email'] = row[2]
        user_data['password'] = row[3]
        user_data['username'] = row[4]
        user_data['public_id'] = row[5]
            

        
        return {'user':user_data}
            