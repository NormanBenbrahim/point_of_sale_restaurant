import os
from typing import List
from flask import current_app
from sqlalchemy.orm import backref

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
            msg = "find_by_id utility called inside ordermodel"
            current_app.logger.info(msg)
            return cls.query.filter_by(order_id=__id).first()

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        """
        utility to find all orders in the database
        """
        try:
            msg = "find_all utility called inside order models"
            current_app.logger.info(msg)
            return cls.query.all()

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    def save_to_db(self) -> None:
        """
        save order to the database
        """
        try:
            current_app.logger.info("Adding order to database")

            db.session.add(self)
            db.session.commit()

            current_app.logger.info("Successfully added order")

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    def delete_from_db(self) -> None:
        """
        delete order from the database
        """
        try:
            current_app.logger.info("Deleting order from database")

            db.session.delete(self)
            db.session.commit()

            current_app.logger.info("Successfully deleted order")

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    def update_from_db(self, **kwargs) -> None:
        """
        update item from database
        """
        try:
            current_app.logger.info("Updating items from database")
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()


class ItemIDsModel(db.Model):
    """
    main models for our items ids found inside the orders
    """
    __tablename__ = "items_ids_table"

    item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey(OrderModel.order_id))
