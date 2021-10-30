import os
import traceback
from flask import current_app
from typing import List

from app.extensions import db


class MenuModel(db.Model):
    """
    main models for our items found inside the menus
    """
    __bindkey__ = os.environ['POSTGRES_DB']
    __tablename__ = "menu_table"

    item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))
    price = db.Column(db.Float())
    quantity = db.Column(db.Integer())


    @classmethod
    def find_by_id(cls, _id: int) -> "MenuModel":
        """
        utility to search for item, see routes for usage
        """
        current_app.logger.info("find_by_id subroutine called")
        
        return cls.query.filter_by(item_id=_id).first()


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
        save item to the database
        """
        current_app.logger.info("Adding item to database")
        
        db.session.add(self)
        db.session.commit()

        current_app.logger.info("Successfully added item")


    def delete_from_db(self) -> None:
        """
        delete item from the database
        """
        current_app.logger.info("Deleting item from database")

        db.session.delete(self)
        db.session.commit()

        current_app.logger.info("Successfully deleted item")


    def update_from_db(self, **kwargs) -> None:
        """
        update item from database
        """
        current_app.logger.info("Updating items from database")
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        current_app.logger.info("Updated items")