from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# app specific extensions, add to extensions method in app.py
jwt = JWTManager()
db = SQLAlchemy()
marshmallow = Marshmallow()


# initializes the blocklist of the jwt tokens, couldn't get this to work
# usually this is best done through redis, but i couldn't get redis to work either
BLOCKLIST = set() 