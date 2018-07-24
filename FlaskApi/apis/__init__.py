from flask_restplus import Api

from .entry import api as ns1


api = Api(
    title='My Diary',
    version='1.0',
    description='My Diary is a flask app that allows a user to update his or her journal on a daily basis',
    # All API metadatas
)

api.add_namespace(ns1, path='/mydiary/v1/entries')
