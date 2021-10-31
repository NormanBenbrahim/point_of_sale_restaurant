import traceback
from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from marshmallow import ValidationError

from app.models.menu import MenuModel
from app.models.orders import OrderModel
from app.schemas.menu import MenuSchema
from app.schemas.orders import OrderSchema
from app.extensions import db, app_error


# initiate schemas
menu_schema = MenuSchema()
menu_list_schema = MenuSchema(many=True)
order_schema = OrderSchema()


class MenuAdd(Resource):
    """
    restful interface for adding menu items
    """
    @classmethod
    def post(cls):
        f"""
        route to add a menu item by id

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['ROUTE_MENU']}")

            current_app.logger.info(f"Looking for menu in database")

            # validation error separately to return custom error messages
            try:
                current_app.logger.info(f"Defining session and passing to the load session")
                #session = scoped_session(sessionmaker(bind=engine))
                session = db.session()
                item = menu_schema.load(request.get_json(), session=session)

            except ValidationError as err:
                current_app.logger.error(f"There was an error in your payload: {err.messages}")
                return {"message": current_app.config['MSG_VALIDATION_ERROR'].format(err.messages)}, 400                


            if MenuModel.find_by_id(item.item_id):
                current_app.logger.warning(f"Item '{item.item_id}' in '{MenuModel.__tablename__}' database")
                return {"message": current_app.config['MSG_ITEM_EXISTS'].format(item.item_id)}, 400

            current_app.logger.info("Saving item to database")
            MenuModel.save_to_db(item)

            current_app.logger.info(f"Menu '{item.item_id}' in '{MenuModel.__tablename__}' database")
            return {"added": menu_schema.dump(item)}, 200        
        
        except BaseException:     
            current_app.logger.error(f"There was an application error: {traceback.format_exc()}")
            return app_error()


class MenuItem(Resource):
    """
    restful interface for adding/querying items in the menu
    """
    @classmethod
    def get(cls, item_id: int):
        f"""
        route to lookup a menu item

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_ITEM']}
        """
        try:
            current_app.logger.info(f"GET Call to route {current_app.config['ROUTE_MENU_ITEM']}")

            current_app.logger.info("Looking or item in database")
            item = MenuModel.find_by_id(item_id)

            # handle item not exist
            if not item:
                current_app.logger.warning(f"Item {item_id} not found, caught error")
                return {"message": current_app.config['MSG_ITEM_NOT_FOUND'].format(item_id)}, 404

            current_app.logger.info(f"Item '{item.item_id}' in '{MenuModel.__tablename__}' database")
            return menu_schema.dump(item), 200

        except BaseException:
            current_app.logger.error(f"There was an application error: {traceback.format_exc()}")
            return app_error()


    @classmethod
    def delete(cls, item_id: int):
        f"""
        route to delete a menu item

        postman request:
        DELETE {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_ITEM']}
        """
        try:
            current_app.logger.info(f"DELETE Call to route {current_app.config['ROUTE_MENU_ITEM']}")

            current_app.logger.info("Looking for item")
            item = MenuModel.find_by_id(item_id)

            # handle item not exist
            if not item:
                current_app.logger.info(f"User {item_id} not found, no delete necessary")
                return{"message": current_app.config['MSG_ITEM_NOT_FOUND'].format(item_id)}, 200

            # delete item
            current_app.logger.info("Deleting item")
            item.delete_from_db()

            current_app.logger.info(f"Successfully deleted {item_id}")
            return {"message": current_app.config['MSG_ITEM_DELETED'].format(item_id)}, 200

        except BaseException:
            current_app.logger.error(f"There was an application error: {traceback.format_exc()}")
            return app_error()


    @classmethod
    def put(cls, item_id: int):
        f"""
        route to update full menu by id

        postman request:
        PUT {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}
        """
        try:
            current_app.logger.info(f"PUT call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU']}")
            
            current_app.logger.info(f"Checking if menu exists")
            item = MenuModel.find_by_id(item_id)
            
            # add item if not exists
            if item is None:
                current_app.logger.info(f"Item {item_id} not found, creating")

                # handle validation errors
                try:
                    # define session
                    current_app.logger.info(f"Defining session and passing to the load session")
                    session = scoped_session(sessionmaker(bind=engine))
                    item = menu_schema.load(request.get_json(), session=session)
                
                except ValidationError as err:
                    current_app.logger.warning(f"There was an error in your payload: {err.messages}")
                    return {"message": current_app.config['MSG_VALIDATION_ERROR'].format(err.messages)}, 400
                
                current_app.logger.info("Added menu item")
                return {"message": current_app.config['MSG_MENU_UPDATED']}, 201

            # update menu
            current_app.logger.info("Updating menu item to database")
            item.update_from_db()

            current_app.logger.info(f"Successfully added {item_id}")
            return {"updated": menu_schema.dump(item)}, 200

        except BaseException:
            current_app.logger.error(f"There was an application error: {traceback.format_exc()}")
            return app_error()


class MenuList(Resource):
    """
    restful interface to list all menus
    """
    @classmethod
    def get(cls):
        f"""
        route to list all menus

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_LIST']}
        """
        try:
            current_app.logger.info(f"GET call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_MENU_LIST']}")
            return {"items": menu_list_schema.dump(MenuModel.find_all())}, 200

        except BaseException:
            current_app.logger.error(f"There was an application error: {traceback.format_exc()}")
            return {"There was an application error. traceback: ": f"{traceback.format_exc()}"}


class OrderAdd(Resource):
    """
    restful interface to add orders by id
    """
    @classmethod
    def post(cls):
        f"""
        route to place an order with a list of ids

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_ORDER']}
        """
        try:
            current_app.logger.info(f"POST call to route {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_ORDER']}")

            # validation error separately to return custom error messages
            try:
                current_app.logger.info(f"Defining session and passing to the load session")
                #session = scoped_session(sessionmaker(bind=engine))
                session = db.session()
                order = order_schema.load(request.get_json(), session=session)

            except ValidationError as err:
                current_app.logger.error(f"There was an error in your payload: {err.messages}")
                return {"message": current_app.config['MSG_VALIDATION_ERROR'].format(err.messages)}, 404

            # check if order with order id already exists in the database
            if OrderModel.find_by_id(order.order_id):
                return {"message": current_app.config['MSG_ORDER_EXISTS'].format(order.order_id)}, 400
            
            # check if the payment amount is enough for the order
            current_app.logger.info("Checking if payment is correct for the items")

            total_due = 0
            for item in order['items']:
                menu_item = MenuModel.find_by_id(item['item_id'])
                if not menu_item:
                    current_app.logger.warning(f"order {order.order_id} has invalid menu item (not exist): {item['item_id']}")
                    return {f"order {order.order_id}": current_app.config['MSG_ITEM_NOT_FOUND'].format(item['item_id'])}
                
                values = menu_schema.dump(menu_item)
                if item['quantity'] > values['quantity']:
                    current_app.logger.warning(f"Insufficient quantity for item {item['item_id']} on order {order.order_id}")
                    return {"message": f"Insufficient quantity for item with id {item['item_id']}, there are {values['quantity']} available on the menu"}, 400
                
                total_due += values['price']*item['quantity']
            
            if total_due > order['payment_amount']:
                current_app.logger.warning(f"Payment insufficient on order {order.order_id}")
                return {"message": f"Payment insufficient. Total due: ${total_due}, \
                                     payment amount: ${order['payment_amount']}, remaining amount due: ${total_due-order['payment_amount']}"}, 400

            current_app.logger.info("Saving to database")
            OrderModel.save_to_db(order)

            return {"added": order_schema.dump(order)}, 200

        except BaseException:
            return app_error()
