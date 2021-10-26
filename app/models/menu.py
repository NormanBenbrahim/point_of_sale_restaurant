from typing import List
from flask import current_app, json
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
# as it is serialized
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


class MenuModel(db.Model):
    """
    main model for our menubase, errors handled in menu routes
    """
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    items = db.Column(MutableDict.as_mutable(JSONEncodedDict), nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu = db.relationship("MenuModel")


    @classmethod
    def find_by_id(cls, name: str) -> "MenuModel":
        """
        utility to search for menus by name in the database
        """
        current_app.logger.info("find_by_name utility called")
        return cls.query.filter_by(name=name).first()


    @classmethod
    def find_all(cls) -> List['MenuModel']:
        """
        utility to find all menus in the database
        """
        current_app.logger.info("find_all utility called")
        return cls.query.all()


    def save_to_db(self) -> None:
        """
        save menu to database
        """
        current_app.logger.info("Saving to database")
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self) -> None:
        """
        delete menu from database
        """
        current_app.logger.info("Deleting from database")
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, **kwargs) -> None:
        """
        update menu item
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)