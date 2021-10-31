import traceback
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# app specific extensions, add to extensions method in app.py
db = SQLAlchemy()
ma= Marshmallow()


def app_error():
    """
    helper function to return traceback in the request
    """
    return {"There was an application error. traceback: ": f"{traceback.format_exc()}"} 
