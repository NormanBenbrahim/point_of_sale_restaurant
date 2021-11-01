from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from app.models.menu import MenuModel
from app.models.orders import OrderModel
from app.schemas.menu import MenuSchema
from app.schemas.orders import OrderSchema
from app.extensions import db, app_error


# initiate schemas
menu_schema = MenuSchema()
menu_list_schema = MenuSchema(many=True)
order_schema = OrderSchema()
order_list_schema = OrderSchema(many=True)


class MenuAdd(Resource):
    """
    restful interface for adding menu items
    """
    @classmethod
    def post(cls):
        f"""
        route to add a menu item by id

        postman request:
        POST {current_app.config['ROUTE_MENU']}
        """
        try:
            msg = f"GET call to route {current_app.config['ROUTE_MENU']}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking for menu in database")

            # validation error separately to return custom error messages
            try:
                msg = "Defining session and passing to the load session"
                current_app.logger.info(msg)
                session = db.session()
                item = menu_schema.load(request.get_json(), session=session)

            except ValidationError as err:
                msg = current_app.config['MSG_VALIDATION_ERROR']
                msg2 = msg.format(err.messages)
                current_app.logger.error(msg2)
                return {"message": msg}, 400
            except BadRequest as err:
                msg = current_app.config['MSG_VALIDATION_ERROR']
                msg2 = msg.format(err)
                current_app.logger.error(msg2)
                return {"message": msg}, 400

            if MenuModel.find_by_id(item.item_id):
                msg = current_app.config['MSG_ITEM_EXISTS']
                msg2 = msg.format(item.item_id)
                current_app.logger.warning(msg2)
                return {"message": msg}, 200

            current_app.logger.info("Saving item to database")
            item.update_from_db()

            msg = f"Menu '{item.item_id}' in '{MenuModel.__tablename__}'"
            current_app.logger.info(msg)
            return {"added": menu_schema.dump(item)}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
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
        GET {current_app.config['ROUTE_MENU_ITEM']}
        """
        try:
            msg = f"GET Call to route {current_app.config['ROUTE_MENU_ITEM']}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking or item in database")
            item = MenuModel.find_by_id(item_id)

            # handle item not exist
            if not item:
                msg = current_app.config['MSG_ITEM_NOT_FOUND'].format(item_id)
                current_app.logger.warning(msg)
                return {"message": msg}, 404

            msg = current_app.config['MSG_ITEM_ADDED'].format(item_id)
            current_app.logger.info(msg)
            return menu_schema.dump(item), 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def delete(cls, item_id: int):
        f"""
        route to delete a menu item

        postman request:
        DELETE {current_app.config['ROUTE_MENU_ITEM']}
        """
        try:
            route = current_app.config['ROUTE_MENU_ITEM']
            msg = f"DELETE Call to route {route}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking for item")
            item = MenuModel.find_by_id(item_id)

            # handle item not exist
            if not item:
                msg = current_app.config['MSG_ITEM_NOT_FOUND'].format(item_id)
                current_app.logger.warning(msg)
                return{"message": msg}, 404

            # delete item
            current_app.logger.info("Deleting item")
            item.delete_from_db()

            msg = current_app.config['MSG_ITEM_DELETED'].format(item_id)
            current_app.logger.info(msg)
            return {"message": msg}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def put(cls, item_id: int):
        f"""
        route to update full menu by id

        postman request:
        PUT {current_app.config['ROUTE_MENU']}
        """
        try:
            msg = f"PUT call to route {current_app.config['ROUTE_MENU']}"
            current_app.logger.info(msg)

            # handle validation errors
            try:
                # define session
                msg = "Defining session and passing to the load session"
                current_app.logger.info(msg)
                session = scoped_session(sessionmaker(bind=engine))
                item = menu_schema.load(request.get_json(),
                                        session=session)

            except ValidationError as err:
                msg = current_app.config['MSG_VALIDATION_ERROR']
                msg2 = msg.format(err.messages)
                current_app.logger.error(msg2)
                return {"message": msg2}, 400
            except BadRequest as err:
                msg = current_app.config['MSG_VALIDATION_ERROR']
                msg2 = msg.format(err)
                current_app.logger.error(msg2)
                return {"message": msg2}, 400

            # current_app.logger.info("Checking if menu exists")
            # item = MenuModel.find_by_id(item_id)
            
            # # add item if not exists
            # if item is None:
            #     current_app.logger.info(f"Item {item_id} not found, creating")

            #     current_app.logger.info("Added menu item")
            #     return {"message": current_app.config['MSG_MENU_UPDATED']}, 201

            # update menu
            current_app.logger.info("Updating menu item to database")
            item.update_from_db()

            current_app.logger.info(f"Successfully added {item_id}")
            return {"updated": menu_schema.dump(item)}, 201

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
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
        GET {current_app.config['ROUTE_MENU_LIST']}
        """
        try:
            msg = f"GET call to route {current_app.config['ROUTE_MENU_LIST']}"
            current_app.logger.info(msg)
            return {"items": menu_list_schema.dump(MenuModel.find_all())}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()


class OrderAdd(Resource):
    """
    restful interface to add orders by id
    """
    @classmethod
    def post(cls):
        f"""
        route to place an order with a list of ids

        postman request:
        POST {current_app.config['ROUTE_ORDER']}
        """
        try:
            msg = f"POST call to {current_app.config['ROUTE_ORDER']}"
            current_app.logger.info(msg)

            # validation error separately to return custom error messages
            try:
                msg = "Defining session and passing to the load session"
                current_app.logger.info(msg)
                session = db.session()
                order = order_schema.load(request.get_json(), session=session)

            except ValidationError as err:
                msg = current_app.config['MSG_VALIDATION_ERROR']
                msg2 = msg.format(err.messages)
                current_app.logger.error(msg2)
                return {"message": msg2}, 400
            except BadRequest as err:
                msg = current_app.config['MSG_VALIDATION_ERROR'].format(err)
                current_app.logger.error(msg)
                return {"message": msg}, 400

            # check if order with order id already exists in the database
            if OrderModel.find_by_id(order.order_id):
                msg = current_app.config['MSG_ORDER_EXISTS']
                msg2 = msg.format(order.order_id)
                return {"message": msg2}, 400

            # check if the payment amount is enough for the order
            msg = "Checking if payment is correct & there is enough in stock"
            current_app.logger.info(msg)

            order_dump = order_schema.dump(order)
            total_due = 0
            all_updated_items = []
            for item in order_dump['items']:
                menu_item = MenuModel.find_by_id(item['item_id'])
                if not menu_item:
                    msg = current_app.config['MSG_ITEM_NOT_FOUND']
                    msg2 = msg.format(item['item_id'])
                    current_app.logger.warning(msg2)
                    return {"message": msg2}, 404

                # check quantities
                menu_items = menu_schema.dump(menu_item)
                if item['quantity'] > menu_items['quantity']:
                    msg = current_app.config['MSG_ITEM_INSUFFICIENT']
                    msg2 = msg.format(item['item_id'], order.order_id)

                    current_app.logger.warning(msg2)
                    return {"message": msg2}, 400

                # update total amount due
                total_due += menu_items['price']*item['quantity']

                # collect updated menu schemas to update the menu
                new_quantity = menu_items['quantity'] - item['quantity']
                menu_items['quantity'] = new_quantity
                msg = "Loading updated schema & adding to list for later"
                current_app.logger.info(msg)
                updated_item = menu_schema.load(menu_items, session=session)
                all_updated_items.append(updated_item)

            # 2 cases, either they underpaid or overpaid
            if total_due > order_dump['payment_amount']:
                remaining = total_due - order_dump['payment_amount']
                msg = current_app.config['MSG_PAYMENT_INSUFFICIENT']
                msg2 = msg.format(total_due,
                                  order_dump['payment_amount'],
                                  remaining)

                current_app.logger.warning(msg)
                return {"mesage": msg2}, 400

            if total_due < order_dump['payment_amount']:
                msg1 = current_app.config['MSG_PAYMENT_OVERCHARGE']
                remaining = order_dump['payment_amount'] - total_due
                msg2 = msg1.format(total_due,
                                   order_dump['payment_amount'],
                                   remaining)

                current_app.logger.warning(msg2)
                return {"message": msg2}, 400

            # update the menu items
            current_app.logger.info("Updating menu items")
            for update_this in all_updated_items:
                update_this.update_from_db()

            current_app.logger.info("Saving order to database")
            OrderModel.save_to_db(order)

            return {"added. order id": order_dump['order_id']}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()


class OrderItem(Resource):
    """
    restful interface for adding/querying orders
    """
    @classmethod
    def get(cls, order_id: int):
        f"""
        route to lookup a order

        postman request:
        GET {current_app.config['ROUTE_ORDER_ITEM']}
        """
        try:
            msg = f"GET Call to route {current_app.config['ROUTE_ORDER_ITEM']}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking or order in database")
            order = OrderModel.find_by_id(order_id)

            # handle item not exist
            if not order:
                msg = current_app.config['MSG_ORDER_NOT_FOUND'].format(order_id)
                current_app.logger.warning(msg)
                return {"message": msg}, 404

            msg = current_app.config['MSG_ORDER_ADDED'].format(order_id)
            current_app.logger.info(msg)
            return order_schema.dump(order), 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def delete(cls, order_id: int):
        f"""
        route to delete a order

        postman request:
        DELETE {current_app.config['ROUTE_ORDER_ITEM']}
        """
        try:
            route = current_app.config['ROUTE_ORDER_ITEM']
            msg = f"DELETE Call to route {route}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking for order")
            item = OrderModel.find_by_id(order_id)

            # handle item not exist
            if not item:
                msg = current_app.config['MSG_ORDER_NOT_FOUND'].format(order_id)
                current_app.logger.warning(msg)
                return{"message": msg}, 404

            # delete item
            current_app.logger.info("Deleting order")
            item.delete_from_db()

            msg = current_app.config['MSG_ORDER_DELETED'].format(order_id)
            current_app.logger.info(msg)
            return {"message": msg}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def put(cls, order_id: int):
        f"""
        route to update full order by id

        postman request:
        PUT {current_app.config['ROUTE_ORDER_ITEM']}
        """
        try:
            msg = f"PUT call to route {current_app.config['ROUTE_ORDER_ITEM']}"
            current_app.logger.info(msg)

            current_app.logger.info("Checking if order exists")
            order = OrderModel.find_by_id(order_id)

            # add order if not exists
            if order is None:
                current_app.logger.info(f"order {order_id} not found, creating")

                # handle validation errors
                try:
                    # define session
                    msg = "Defining session and passing to the load session"
                    current_app.logger.info(msg)
                    session = scoped_session(sessionmaker(bind=engine))
                    order = order_schema.load(request.get_json(),
                                            session=session)

                except ValidationError as err:
                    msg = current_app.config['MSG_VALIDATION_ERROR']
                    msg2 = msg.format(err.messages)
                    current_app.logger.error(msg2)
                    return {"message": msg2}, 400
                except BadRequest as err:
                    msg = current_app.config['MSG_VALIDATION_ERROR']
                    msg2 = msg.format(err)
                    current_app.logger.error(msg2)
                    return {"message": msg2}, 400

                current_app.logger.info("Added menu order")
                return {"message": current_app.config['MSG_ORDER_UPDATED']}, 201

            # update menu
            current_app.logger.info("Updating menu order to database")
            order.update_from_db()

            current_app.logger.info(f"Successfully added {order_id}")
            return {"updated": order_schema.dump(order)}, 201

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()


class OrderList(Resource):
    """
    restful interface for listing all orders
    """
    @classmethod
    def get(cls):
        f"""
        route to list all orders successfully placed

        postman request:
        GET {current_app.config['ROUTE_ORDER_LIST']}
        """
        try:
            out = {"orders": order_list_schema.dump(OrderModel.find_all())}
            msg = f"GET call to {current_app.config['ROUTE_ORDER_LIST']}"
            current_app.logger.info(msg)
            return out, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()
