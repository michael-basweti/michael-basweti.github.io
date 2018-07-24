"""
entry point to the app
"""
from flask import Flask
from apis import api

app = Flask(__name__)  # pylint: disable=invalid-name
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
