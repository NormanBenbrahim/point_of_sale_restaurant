from app.models.menu import MenuModel, ItemsModel
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, EXCLUDE


class ItemSchema(ma.Schema):
    id = fields.Int()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Integer()
    unknown = EXCLUDE

    class Meta:
        model = ItemsModel
        load_instance = True
        include_fk = True


class MenuSchema(ma.Schema):
    items = fields.Dict(keys=fields.Int(), values=fields.Nested(ItemSchema))

    class Meta:
        model = MenuModel
        load_instance = True
        #include_fk = True

