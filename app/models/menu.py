import os
from flask import current_app
from typing import List

from app.extensions import db
from app.extensions import app_error


class MenuModel(db.Model):
    """
    main models for our items found inside the menus
    """
    __bindkey__ = os.environ['POSTGRES_DB']
    __tablename__ = "menu_table"

    item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    price = db.Column(db.Float())
    quantity = db.Column(db.Integer())

    @classmethod
    def find_by_id(cls, _id: int) -> "MenuModel":
        """
        utility to search for item, see routes for usage
        """
        msg = "find_by_id subroutine called inside menu model"
        current_app.logger.info(msg)

        return cls.query.filter_by(item_id=_id).first()

    @classmethod
    def find_all(cls) -> List['MenuModel']:
        """
        utility to find all menus in the database
        """
        try:
            msg = "find_all utility called inside menu models"
            current_app.logger.info(msg)
            return cls.query.all()

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    def save_to_db(self) -> None:
        """
        save item to the database
        """
        try:
            current_app.logger.info("Adding item to database")

            db.session.add(self)
            db.session.commit()

            current_app.logger.info("Successfully added item")

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    def delete_from_db(self) -> None:
        """
        delete item from the database
        """
        try:
            current_app.logger.info("Deleting item from database")

            db.session.delete(self)
            db.session.commit()

            current_app.logger.info("Successfully deleted item")
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
