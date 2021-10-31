import os
from typing import List
from flask import current_app, json
from sqlalchemy.orm import backref
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable

from app.extensions import db, app_error


class OrderModel(db.Model):
    """
    models for our order
    """
    __bindkey__ = os.environ['POSTGRES_DB']
    __tablename__ = "orders_table"

    order_id = db.Column(db.Integer, primary_key=True)
    items = db.relationship("ItemIDsModel", backref=backref(__tablename__))
    order_note = db.Column(db.String(150))
    payment_amount = db.Column(db.Float)

    
    @classmethod
    def find_by_id(cls, __id: int) -> "OrderModel":
        """
        utility to find order by id
        """
        try:
            current_app.logger.info("find_by_id utility called inside ordermodel")
            return cls.query.filter_by(order_id=__id).first()

        except BaseException:
            return app_error()

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        """
        utility to find all orders in the database
        """
        try:
            current_app.logger.info("find_all utility called inside order models")
            return cls.query_all()

        except BaseException:
            return app_error()


    def save_to_db(self) -> None:
        """
        save order to the database
        """
        current_app.logger.info("Adding order to database")
        
        db.session.add(self)
        db.session.commit()

        current_app.logger.info("Successfully added order")


    def delete_from_db(self) -> None:
        """
        delete order from the database
        """
        current_app.logger.info("Deleting order from database")

        db.session.delete(self)
        db.session.commit()

        current_app.logger.info("Successfully deleted order")


class ItemIDsModel(db.Model):
    """
    main models for our items ids found inside the orders
    """
    __tablename__ = "items_ids_table"

    item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey(OrderModel.order_id))