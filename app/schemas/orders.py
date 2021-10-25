from typing_extensions import Required
from marshmallow import fields, validate, ValidationError 

from app.extensions import marshmallow
from app.models.orders import Orders


def ensure_unique_identity(data):
    """
    helper function to make sure orders are unique
    """
    orders = Orders.find_by_identity(data)

    if user:
        raise ValidationError(f'{data} already exists')

    return data

def ensure_correct_order(order):
    """
    helper function to make sure the order amount is correct
    """
    pass


class OrdersSchema(marshmallow.Schema):
    """
    orders schema should contain 
        -list of item ids with quantity
        -payment amount
        -order note
    
    creating successful order should return order id
    Each route should perform business logic validation to prevent common errors. 
    The order endpoint specifically should enforce payment correctness, and item availability.
    """
    # assume someone can have the same order note for multiple orders if they repeat orders a lot
    order_note = fields.Str(required=True)

    payment_amount = fields.Float(required=True)

    items = fields.Dict(required=True, keys=fields.Str(), values=fields.Str())

    #id = fields.Int(required=True)