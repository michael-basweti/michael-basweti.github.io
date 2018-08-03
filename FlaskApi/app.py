"""
entry point to the app
"""
from flask import Flask
from flask_cors import CORS
from apis import api

app = Flask(__name__)  # pylint: disable=invalid-name
CORS(app)
api.init_app(app)
app.config['SECRET_KEY'] = 'thisismysecretkeynigga'

print('opened database successfully')
if __name__ == '__main__':
    app.run('', port=5000, debug=True)
