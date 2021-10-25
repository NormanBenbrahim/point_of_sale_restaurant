from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# app specific extensions, add to extensions method in app.py
jwt = JWTManager()
db = SQLAlchemy()
marshmallow = Marshmallow()


# initializes the blocklist of the jwt tokens, import directly
# a better solution is to use redis and store these there, but couldn't get it working
BLOCKLIST = set() 