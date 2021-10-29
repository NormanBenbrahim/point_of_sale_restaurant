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
    models for our menu
    """
    __bindkey__ = os.environ['POSTGRES_DB']
    __tablename__ = "menus_table"

    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship("ItemsModel", backref=backref(__tablename__))


class ItemsModel(db.Model):
    """
    main models for our items found inside the menus
    """
    __tablename__ = "items_table"

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey(MenuModel.id))