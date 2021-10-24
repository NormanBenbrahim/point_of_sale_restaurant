from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


debug_toolbar = DebugToolbarExtension() # useful if we add swagger docs to this later
jwt = JWTManager()
db = SQLAlchemy()
marshmallow = Marshmallow()
