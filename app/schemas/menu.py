from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.menu import MenuModel


class MenuSchema(SQLAlchemyAutoSchema):
    """
    schema for menu & items
    """
    
    class Meta:
        """
        get sqlalchemy to autofill the schema fields
        """
        model = MenuModel
        include_relationships = True
        load_instance = True
        include_fk = True