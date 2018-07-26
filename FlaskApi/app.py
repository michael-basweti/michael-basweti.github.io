"""
entry point to the app
"""
from flask import Flask
import psycopg2
from apis import api

app = Flask(__name__)  # pylint: disable=invalid-name
api.init_app(app)
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'


print('opened databse successfully')
app.run(debug=True)
