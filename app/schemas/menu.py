from marshmallow.decorators import pre_dump
from marshmallow.exceptions import ValidationError
from app.models.menu import MenuModel, ItemsModel
from app.extensions import ma
from app.extensions import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, EXCLUDE, post_load


class Nested(fields.Nested):
    """
    as far as i know deserializing nested objects is still an outstanding issue
    for the marshmallow team so a custom nested object is necessary
    
    see:
    https://github.com/marshmallow-code/marshmallow-sqlalchemy/issues/67
    https://stackoverflow.com/questions/63267893/sqlalchemyautoschema-nested-deserialization
    """
    def _deserialize(self, *args, **kwargs):
        if hasattr(self.schema, "session"):
            self.schema.session = db.session  # overwrite session here
            self.schema.transient = self.root.transient
        return super()._deserialize(*args, **kwargs)


class ItemSchema(SQLAlchemyAutoSchema):
    """
    item schema
    """
    item_id = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    @validates('quantity')
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0")

    @validates('price')
    def validate_price(self, price):
        if price < 0:
            raise ValidationError("Price must be greater than 0")


    class Meta:
        model = ItemsModel
        load_instance = True
        include_fk = True
        #unknown = EXCLUDE


class MenuSchema(SQLAlchemyAutoSchema):
    """
    menu schema

    payload example:
    {
        "items": [
            {"id": "1", "price": "4.99", "description": "hamburger"},
            {"id": "2", "price": "7.99", "description": "french fries"},
            ...,
            {"id": "n", "price": "12.99", "description": "royale with cheese"}
        ]
    }
    """
    items = Nested(ItemSchema, many=True)

    class Meta:
        model = MenuModel
        load_instance = True
        include_fk = True
        #unknown = EXCLUDE

