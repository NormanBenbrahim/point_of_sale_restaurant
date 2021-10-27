import traceback
from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.models.menu import MenuModel
from app.schemas.menu import ItemSchema, MenuSchema
from app.extensions import jwt


# initiate schemas
menu_schema = MenuSchema()
menu_list_schema = MenuSchema(many=True)
item_list_schema = ItemSchema(many=True)


class Menu(Resource):
    """
    restful interface for menu
    """
    @classmethod
    #@jwt_required()
    def get(cls, menu_id: int):
        f"""
        route to list a menu by id

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['ROUTE_MENU']}")

            current_app.logger.info(f"Looking for menu in database")
            menu = MenuModel.find_by_id(menu_id)

            if menu is None:            
                current_app.logger.warning(f"Menu '{menu_id}' not found in '{MenuModel.__tablename__}' database")
                return {"message": current_app.config['MSG_MENU_NOT_FOUND']}, 400

            current_app.logger.info(f"Menu '{menu_id}' in '{MenuModel.__tablename__}' database")
            return menu_schema.dump(menu), 200        
        
        except BaseException:     
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    @classmethod
    #@jwt_required()
    def post(cls, menu_id: int):
        f"""
        route to add a full menu by id

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"POST call to route {current_app.config['ROUTE_MENU']}")

            # duplicate menus
            current_app.logger.info(f"Checking if menu already exists")
            menu = MenuModel.find_by_id(menu_id)
            
            if menu is not None:
                current_app.logger.warning(f"Menu '{menu_id}' found in '{MenuModel.__tablename__}' database")
                return {"message": current_app.config['MSG_MENU_ALREADY_EXISTS'].format(menu_id)}, 400

            # error handling
            current_app.logger.info("Menu doesn't exist, checking payload")
            payload = request.json()

            current_app.logger.info(f"Defining session and passing to the load session")
            session = scoped_session(sessionmaker(bind=engine))
            menu = menu_schema.load(payload, session=session)
            
            # add new menu
            current_app.logger.info("Saving menu to database")
            MenuModel.save_to_db(menu)

            current_app.logger.info(f"Successfully added {menu}")
            return {"message": current_app.config['MSG_MENU_ADDED']}, 200

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    @classmethod
    #@jwt_required()
    def delete(cls, menu_id: int):
        f"""
        route to delete menu full menu by id

        postman request:
        DELETE {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"DELETE call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}")

            current_app.logger.info("Looking for menu in database")
            menu = MenuModel.find_by_id(menu_id)

            if menu is not None:
                current_app.logger.info("Deleting menu")
                menu.delete_from_db()

                current_app.logger.info(current_app.config['MSG_MENU_DELETED'])
                return {"message": current_app.config['MSG_MENU_DELETED']}, 200
            
            current_app.logger.warning(current_app.config['MSG_MENU_NOT_FOUND'])
            return {"message": current_app.config['MSG_MENU_NOT_FOUND']}, 404

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


    @classmethod
    #@jwt_required()
    def put(cls, menu_id: int):
        f"""
        route to update full menu by id

        postman request:
        PUT {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"PUT call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}")
            
            current_app.logger.info(f"Checking if menu exists")
            menu = MenuModel.find_by_id(menu_id)
            # update menu if exists

            if menu is not None:
                current_app.logger.info(f"Menu {menu_id} found, updating fields")

                # define session
                #current_app.logger.info(f"Defining session and passing to the load session")
                #session = scoped_session(sessionmaker(bind=engine))

                #menu = menu_schema.load(request.get_json(), session=session)
                payload = request.get_json()
                menu.update_from_db(payload[menu_id])
                
                return {"message": current_app.config['MSG_MENU_UPDATED']}, 201

            # add new menu
            current_app.logger.info("Saving menu to database")
            MenuModel.save_to_db(menu)

            current_app.logger.info(f"Successfully added {menu}")
            return {"message": current_app.config['MSG_MENU_ADDED']}, 200


        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


class MenuItem(Resource):
    """
    restful interface for menu items
    """
    @classmethod
    @jwt_required()
    def get(cls, menu_id: int, item_id: int):
        f"""
        route to list a menu item by menu id and item id

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_ITEM']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['ROUTE_MENU_ITEM']}")

            current_app.logger.info(f"Looking for menu in database")
            menu = MenuModel.find_by_id(menu_id)

            if menu is None:
                current_app.logger.info(f"Menu '{menu_id}' in '{MenuModel.__tablename__}' database")
                return menu_schema.dump(menu), 200
            
            current_app.logger.warning(f"Menu '{menu_id}' not found in '{MenuModel.__tablename__}' database")
            return {"message": current_app.config['MSG_MENU_NOT_FOUND']}, 400
        
        except BaseException:     
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")  


class MenuList(Resource):
    """
    restful interface to list all menus
    """
    @classmethod
    #@jwt_required()
    def get(cls):
        f"""
        route to list all menus

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_LIST']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_LIST']}")
            return {"menus": menu_list_schema.dump(MenuModel.find_all())}, 200

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


class ItemList(Resource):
    """
    restful interface to list all items in a menu
    """
    @classmethod
    #@jwt_required()
    def get(cls, item_id: int):
        f"""
        route to list all menus

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_ITEM_LIST']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_ITEM_LIST']}")
            
            current_app.logger.info(f"Looking for menu in database")
            menu = MenuModel.find_by_id(item_id)

            if menu is not None:
                current_app.logger.info(f"Menu found, listing items")
                return {"items": menu_list_schema.dump(MenuModel.find_all())}, 200

            current_app.logger.info("Menu items not found")
            return {"message": current_app.config['MSG_MENU_ITEM_NOT_FOUND']}, 400

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")