"""
entry point to the app
"""
from flask import Flask
import psycopg2
from apis import api
from flask_cors import CORS

app = Flask(__name__)  # pylint: disable=invalid-name
CORS(app)
api.init_app(app)
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'
#conn = psycopg2.connect(database="df4keijp3j4gsn",user="cslzrgdwqphsdg",password="1f370b6b19a69f6aab5cb73d09fc1edfc4a7eee53680458d01ed498c777b1932",host="ec2-23-23-242-163.compute-1.amazonaws.com")

print('opened database successfully')
if __name__ == '__main__':
    app.run('',port=5000,debug=True)
