import traceback
import os
from typing import List
from flask import current_app, json
from sqlalchemy.orm import backref
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable

from app.extensions import db


class MenuModel(db.Model):
    """
    menu will be modeled as so:
    {
        1: {
            1: {
                "description": "a piece of tomato",
                "price": 0.64,
                "quantity": 1
                },
            2: {
                "description": "a hamburger with cheese",
                "price": 9.95,
                "quantity": 2
                }
        },
        2: {....},
        ...,
        n: {...}
    }
    """
    __bindkey__ = os.environ['POSTGRES_DB']
    __tablename__ = "menus_table"

    id = db.Column(db.Integer, primary_key=True)


class ItemsModel(db.Model):
    """
    main models for our items found inside the menus
    """
    __tablename__ = "items_table"

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey(MenuModel.id))
    items = db.relationship("MenuModel", backref=backref(__tablename__))
