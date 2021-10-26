from typing import List
from flask import current_app

from app.extensions import db

class MenuModel(db.Model):
    """
    main model for our menubase, errors handled in menu routes
    """
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    #items = db.Column(db.PickleType, nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu = db.relationship("MenuModel")


    @classmethod
    def find_by_name(cls, name: str) -> "MenuModel":
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