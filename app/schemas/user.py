from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.user import UserModel


class UserSchema(SQLAlchemyAutoSchema):
    """
    schema for users to login
    """

    class Meta:
        """
        get sqlalchemy to autofill the schema fields
        """
        model = UserModel
        include_relationships = True
        load_instance = True
