from flask_sqlalchemy import model
#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.menu import MenuModel, ItemsModel
from app.extensions import marshmallow


#class MenuSchema(SQLAlchemyAutoSchema):
class MenuSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    schema for menus
    """
    class Meta:
        """
        get sqlalchemy to autofill the schema fields
        """
        model = MenuModel
        #include_relationships = True
        #load_instance = True
        #include_fk = True


#class ItemSchema(SQLAlchemyAutoSchema):
class ItemSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    schema for items inside menus
    """
    class Meta:
        model = ItemsModel
    
    items = marshmallow.Nested(MenuSchema)