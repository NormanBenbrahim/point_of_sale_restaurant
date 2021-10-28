from flask_sqlalchemy import model
from marshmallow.decorators import post_load

from app.models.menu import MenuModel, ItemsModel
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate


class ItemSchema(ma.Schema):
    #id = fields.Int()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Integer()

    # class Meta:
    #     model = ItemsModel
    #     load_instance = True


class MenuSchema(ma.Schema):
    items = fields.Dict(keys=fields.Int(), values=fields.Nested(ItemSchema))

    # class Meta:
    #     model = MenuModel





# class MenuSchema(ma.SQLAlchemyAutoSchema):
#     """
#     schema for menus
#     """
#     items = fields.Relationship
#     class Meta:
#         """
#         get sqlalchemy to autofill the schema fields
#         """
#         model = MenuModel
#         include_relationships = True
#         load_instance = True
#         #include_fk = True


# class ItemSchema(ma.SQLAlchemyAutoSchema):
#     """
#     schema for nested items inside menus
#     """
#     class Meta:
#         model = ItemsModel
    
#     items = ma.Nested(MenuSchema, many=True)
