"""
entry point to the app
"""
from flask import Flask
import psycopg2
from apis import api

app = Flask(__name__)  # pylint: disable=invalid-name
api.init_app(app)
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'
conn = psycopg2.connect(database="mydiary", user="postgres",  # pylint: disable=invalid-name
                        password="trizabas2017", host="127.0.0.1", port="5432")

print('opened databse successfully')
app.run(debug=True)
