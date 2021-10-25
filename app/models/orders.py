#from lib.util_sqlalchemy import ResourceMixin
from flask import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator

from app.extensions import db


MAXCHARSIZE = 100


class ItemsPickleType(TypeDecorator):
    """
    create a new column type in order to store a dict of values (the items in the order) and be able to 
    serialize/deserialize the objects 

    see 
    https://stackoverflow.com/questions/1378325/python-dicts-in-sqlalchemy
    https://docs.sqlalchemy.org/en/14/orm/extensions/mutable.html#establishing-mutability-on-scalar-column-values
    """
    impl = sqlalchemy.Text(MAXCHARSIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Orders(db.Model):
    """
    database model for orders table
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)

    # assume we only let them record 300 characters in the note since order
    # receipts (physical receipts) are pretty small
    order_note = db.Column(db.string(300), server_default='', nullable=False)

    payment_amount = db.Column(db.Float(), nullable=False)

    items = db.Column(ItemsPickleType())
