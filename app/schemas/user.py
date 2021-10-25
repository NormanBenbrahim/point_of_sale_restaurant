from app.extensions import marshmallow
from app.models.user import UserModel
from flask import current_app


class UserSchema(marshmallow.Schema):
    """
    schema for users to login
    """
    
    class Meta:
        model = UserModel
        load_only = ("password")
        dump_only = ("id")
