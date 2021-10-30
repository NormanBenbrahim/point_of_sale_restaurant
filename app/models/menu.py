import os
from flask import current_app

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