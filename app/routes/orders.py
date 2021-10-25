from flask import Blueprint, jsonify

from app.extensions import db 

orders_route = Blueprint('orders-route', __name__)


@orders_route.route('/orders/<int:id>', methods=['GET'])
def get_orders(id):
    """"
    list a specific orders item by id
    """

    # dummy response
    # return jsonify({'id': id})


@orders_route.route('/orders/all', methods=['GET'])
def get_all_orderss():
    """"
    list all the orders
    """
    # dummy response
    return jsonify({'orders': {"order1": "one", "order2": "two"}})


@orders_route.route('/orders/<int:id>/<item>', methods=['POST'])
def update_orders(id, item):
    """
    update item by id
    """
    return jsonify({"updated": id, "item": item})


