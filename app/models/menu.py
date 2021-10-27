import traceback
from typing import List
from flask import current_app, json
#from sqlalchemy.orm import backref
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable

from app.extensions import db


# from sqlalchemy docs, helps map dictionaries as json string
class JSONEncodedDict(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# from sqlalchemy docs, applies mutable mixin to dictionary to allow to update in place
# as it is serialized, helper class for above class
class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


# wrapping everything in trys to hopefully catch in logs
class MenuModel(db.Model):
    """
    menu will be modeled as so:

    {
        {"<int:main_id>": {
            "<int:item_id>": {
                "price": <float>, 
                "description": <str>,
                "quantity": <int>
                },
            "<int:item_id>": {
                "price": <float>, 
                "description": <str>,
                "quantity": <int>
                },
            {...}
            } 
        }
    }
    """
    __tablename__ = "menus_table"

    id = db.Column(db.Integer, primary_key=True)

    # items into general purpose mutable dict & parse errors in route
    #items = db.Column(MutableDict.as_mutable(JSONEncodedDict), nullable=False)
    items = db.relationship("ItemsModel", backref='menus', lazy="dynamic")

    # link the menu and orders tables' ids together for easy lookup
    #order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    #order = db.relationship("OrderModel")


    @classmethod
    def find_by_id(cls, menu_id: int) -> "MenuModel":
        """
        utility to search for menus by id in the database
        """
        try:
            current_app.logger.info("find_by_id utility called inside menu models")
            return cls.query.filter_by(id=menu_id).first()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    @classmethod
    def find_all(cls) -> List['MenuModel']:
        """
        utility to find all menus in the database
        """
        try:
            current_app.logger.info("find_all utility called inside menu models")
            return cls.query.all()
        
        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def save_to_db(self) -> None:
        """
        save menu to database
        """
        try:
            current_app.logger.info("Saving to database")
            db.session.add(self)
            db.session.commit()
        
        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def delete_from_db(self) -> None:
        """
        delete menu from database
        """
        try:
            current_app.logger.info("Deleting from database")
            db.session.delete(self)
            db.session.commit()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def update_from_db(self, **kwargs) -> None:
        """
        update menu item
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ItemsModel(db.Model):
    """
    main models for our items found inside the menus
    """
    __tablename__ = "items_table"

    items_id = db.Column(db.Integer, db.ForeignKey(MenuModel.id), primary_key=True)
    items = db.Column(MutableDict.as_mutable(JSONEncodedDict))

    @classmethod
    def find_by_id(cls, _id2: int) -> "ItemsModel":
        """
        utility to search for menus by id in the database
        """
        try:
            current_app.logger.info("find_by_id utility called inside items models")
            return cls.query.filter_by(id=_id2).first()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")

    @classmethod
    def find_all(cls) -> List['ItemsModel']:
        """
        utility to find all menus in the database
        """
        try:
            current_app.logger.info("find_all utility called inside items models")
            return cls.query.all()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def save_to_db(self) -> None:
        """
        save item to items database
        """
        try:
            current_app.logger.info("Saving to database")
            db.session.add(self)
            db.session.commit()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def delete_from_db(self) -> None:
        """
        delete item from items database
        """
        try:
            current_app.logger.info("Deleting from database")
            db.session.delete(self)
            db.session.commit()

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    def update_from_db(self, **kwargs) -> None:
        """
        update menu item
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")