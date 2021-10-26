#import requests
from flask import current_app, request

routes = """
ROUTE_USER_REGISTER = '/register'
ROUTE_USER = '/user/<int:user_id>'
ROUTE_LOGIN = '/login'
ROUTE_LOGOUT = '/logout'
ROUTE_REFRESH = '/refresh'
"""

class TestAPI(object):
    def test_success_route(self):
        """
        main endpoint is working
        """
        url = current_app.config['SERVER_NAME'] + current_app.config['ROUTE_SUCCESS']
        response = request.get(url)
        assert response.status_code ==  200


    def test_login_route(self):
        """
        login route is working
        """
        url = current_app.config['SERVER_NAME'] + current_app.config['ROUTE_LOGIN']
        response = request.get(url)
        assert response.status_code ==  200


    def test_login_route(self):
        """
        login route is working
        """
        url = current_app.config['SERVER_NAME'] + current_app.config['ROUTE_LOGIN']
        response = request.get(url)
        assert response.status_code ==  200


    def test_user_route(self):
        """
        test user route is working
        """
        url = current_app.config['SERVER_NAME'] + current_app.config['ROUTE_USER']
        response = request.get(url)
        assert response.status_code ==  200