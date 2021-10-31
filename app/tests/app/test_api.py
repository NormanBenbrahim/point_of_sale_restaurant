#import requests
from flask import current_app

all_routes = """
ROUTE_USER_REGISTER = '/register'
ROUTE_USER = '/user/<int:user_id>'
ROUTE_LOGIN = '/login'
ROUTE_LOGOUT = '/logout'
ROUTE_REFRESH = '/refresh'
"""

class TestAPI(object):
    def test_success(self, client):
        """
        test main endpoint, should always return 200 if route is right
        """
        route = current_app.config['ROUTE_SUCCESS']
        response = client.get(route)
        req = client.post(route)
        
        assert response.status_code ==  200, f"route '{route}' invalid"
        assert req.status_code == 405

    
    def test_all_items(self, client):
        """
        test all items endpoint, should always return 200 if route is right
        """
        route = current_app.config['ROUTE_MENU_LIST']
        response = client.get(route)
        req = client.post(route)
        
        assert response.status_code ==  200, f"route '{route}' invalid"
        assert req.status_code == 405


    def test_all_orders(self, client):
        """
        test all orders endpoint, should always return 200 if route is right
        """
        route = current_app.config['ROUTE_ORDER_LIST']
        response = client.get(route)
        req = client.post(route)
        
        assert response.status_code ==  200, f"route '{route}' invalid"
        assert req.status_code == 405


    def test_add_item(self, client):
        """
        test adding an item to the menu
        """
        route = current_app.config['ROUTE_MENU']
        response = client.get(route)
        
        # get method isn't allowed for this route
        assert response.status_code == 405


    def test_add_order(self, client):
        """
        test adding an order
        """
        route = current_app.config['ROUTE_ORDER']
        response = client.get(route)

        # method isn't allowed for this route
        assert response.status_code == 405


    # def test_get_item(self, client):
    #     """
    #     test getting item
    #     """
    #     route = current_app.config['ROUTE_MENU_ITEM']
    #     req = client.post(route + "/1")

    #     # method isn't allowed for this route
    #     assert req.status_code == 405


    # def test_get_order(self, client):
    #     """
    #     test getting order
    #     """
    #     route = current_app.config['ROUTE_ORDER_ITEM']
    #     req = client.post(route + '/1')

    #     # method isn't allowed for this route
    #     assert req.status_code == 405