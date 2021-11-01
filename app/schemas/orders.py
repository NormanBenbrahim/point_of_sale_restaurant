from marshmallow.exceptions import ValidationError
from app.models.orders import ItemIDsModel, OrderModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates

from app.extensions import db


class Nested(fields.Nested):
    """
    as far as i know deserializing nested objects is still an outstanding issue
    for the marshmallow team, so we need a custom nested object

    see:
    https://github.com/marshmallow-code/marshmallow-sqlalchemy/issues/67
    https://stackoverflow.com/questions/63267893/sqlalchemyautoschema-nested-deserialization
    """

    def _deserialize(self, *args, **kwargs):
        if hasattr(self.schema, "session"):
            self.schema.session = db.session  # overwrite session here
            self.schema.transient = self.root.transient
        return super()._deserialize(*args, **kwargs)


class ItemIDs(SQLAlchemyAutoSchema):
    """
    item ids
    """
    item_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)

    @validates('quantity')
    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise ValidationError("quantity must be greater than 0")

    @validates('item_id')
    def validate_item_id(self, item_id):
        if item_id < 0:
            raise ValidationError("item_id cannot be negative")

    class Meta:
        model = ItemIDsModel
        load_instance = True
        include_fk = True


class OrderSchema(SQLAlchemyAutoSchema):
    """
    orders

    sample:
    {
        "payment_amount": "34.99",
        "order_note": "a bunch of food",
        "order_id": "1",
        "items": [
            {"item_id": "1", "quantity": "1", "order_id": "1"},
            {"item_id": "2", "quantity": "2", "order_id": "1"},
            {"item_id": "3", "quantity": "4", "order_id": "1"}
            ]
    }
    """
    order_id = fields.Integer(required=True)
    order_note = fields.String(required=True)
    payment_amount = fields.Float(required=True)
    items = Nested(ItemIDs, many=True, required=True)

    # error handling
    @validates('payment_amount')
    def validate_payment_amount(self, payment_amount):
        if payment_amount < 0:
            raise ValidationError("'payment_amount' must be greater than 0")

    @validates('order_note')
    def validate_order_note(self, note):
        if note.strip() == "":
            raise ValidationError("'order_note' cannot be empty")

    @validates('order_id')
    def validate_order_id(self, order_id):
        if order_id < 0:
            raise ValidationError("'order_id' must not be negative")

    class Meta:
        model = OrderModel
        load_instance = True
        include_relationships = True
        include_fk = True
