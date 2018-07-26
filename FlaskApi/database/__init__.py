from flask_sqlalchemy import SQLAlchemy

db = [

]


def reset_database():
    from FlaskApi.database.db import Post  # noqa
    #db.drop_all()
    #db.create_all()