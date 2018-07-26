"""
entry point to the app
"""
from flask import Flask
from apis import api
import psycopg2


app = Flask(__name__)  # pylint: disable=invalid-name
api.init_app(app)
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'
conn = psycopg2.connect(database="mydiary", user="postgres", password="trizabas2017",
host="127.0.0.1", port="5432")

print('opened databse successfully') 


app.run(debug=True)
