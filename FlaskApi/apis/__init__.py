from flask_restplus import Api
from flask import Flask
from .entry import api as ns1
from.user import api as ns2

app = Flask(__name__)  # pylint: disable=invalid-name

authorizations ={
    'apiKey':{
        'type':'apiKey',
        'in':'header',
        'name':'x-access-token'
    }
}



api = Api(
    title='My Diary',
    version='1.0',
    description='My Diary is a flask app that allows a user to update his or her journal on a daily basis',
    # All API metadatas
    authorizations=authorizations
)

api.add_namespace(ns1, path='/mydiary/v1/entries')
api.add_namespace(ns2, path='/user/v1/actions')