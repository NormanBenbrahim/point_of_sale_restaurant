from marshmallow.exceptions import ValidationError
from app.models.menu import MenuModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates


class MenuSchema(SQLAlchemyAutoSchema):
    """
    item schema

    sample:
    {
        "item_id": "1",
        "description": "a royale with cheese",
        "price": "9.99",
        "quantity": "12"
    }
    """
    item_id = fields.Integer(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    # error handling
    @validates('quantity')
    def validate_quantity(self, quantity):
        if quantity < 0:
            raise ValidationError("'quantity' must be greater than 0")

    @validates('price')
    def validate_price(self, price):
        if price < 0:
            raise ValidationError("'price' must be greater than 0")

    @validates('description')
    def validate_description(self, description):
        if description.strip() == '':
            raise ValidationError("'description' must not be empty")

    @validates('item_id')
    def validate_item_id(self, item_id):
        if item_id < 0:
            raise ValidationError("'item_id' must not be negative")

    class Meta:
        model = MenuModel
        load_instance = True
        include_relationships = True
