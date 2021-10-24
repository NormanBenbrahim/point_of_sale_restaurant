from flask import Blueprint, jsonify

menu_route = Blueprint('menu-route', __name__)


@menu_route.route('/menu/<int:id>', methods=['GET'])
def get_menu(id):
    """"
    list a specific menu item by id
    """
    # dummy response
    return jsonify({'id': id})


@menu_route.route('/menu', methods=['GET'])
def get_all_menus():
    """"
    list all items in the menu
    """
    # dummy response
    return jsonify({'menu': {"item1": "one", "item2": "two"}})


@menu_route.route('/menu/<int:id>/<item>', methods=['POST'])
def update_menu(id, item):
    """
    update item by id
    """
    return jsonify({"updated": id, "item": item})


