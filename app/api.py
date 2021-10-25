import traceback
import logging
from flask import Flask
from flask_restful import Api
#from flask_jwt_extended import JWTManager

from app.extensions import db, jwt, marshmallow
from app.routes.success import Success
from app.routes.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
#from app.routes.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
#from app.routes.index import index_route
#from app.routes.menu import menu_route
#from app.routes.orders import orders_route
#from app.routes.healthcheck import healthcheck_route

# setup logger
logging.basicConfig(level=logging.DEBUG, # change to  
                    format=f'%(asctime)s [%(levelname)s] %(name)s %(threadName)s : %(message)s')

def create_app(settings_override=None):
    """
    create app function for dockerfile entry
    """
    try:
        # initialize app & define config scopes
        app = Flask(__name__, instance_relative_config=True)
        app.logger.info("Initialized app")

        app.config.from_object('config.settings')
        app.config.from_pyfile('settings.py', silent=True)
        app.logger.info("Loaded settings")

        if settings_override:
            app.config.update(settings_override)

        # add extensions
        extensions(app)
        
        # make api
        api = Api(app)

        # create tables
        @app.before_first_request
        def create_tables():
            db.create_all()

        # check if token blocklisted, best to use redis but sadly i couldn't get it to work
        @jwt.token_in_blocklist_loader
        def check_if_blocklist(token):
            return token['jti'] in BLOCKLIST

        # add routes, '/' first is best practice
        api.add_resource(Success, app.config['ROUTE_SUCCESS'])

        # user routes
        api.add_resource(UserLogin, app.config['ROUTE_LOGIN'])
        api.add_resource(UserRegister, app.config['ROUTE_USER_REGISTER'])

        # orders route

        # menu route


        #api.add_resource(User)
        #app.register_blueprint(menu_route)
        #app.register_blueprint(orders_route)

        return app

    # base exception to catch everything & spit it out otherwise debugging in docker sucks
    except BaseException:
        print("There was an error while creating the application: \n" + traceback.format_exc())


def extensions(app):
    """
    register each loaded extension to the app, keep dir structure clean
    """
    jwt.init_app(app)
    db.init_app(app)
    marshmallow.init_app(app)

    return None 

# def jwt_callbacks():
#     """
#     Set up custom behavior for JWT based authentication.

#     :return: None
#     """
#     @jwt.user_loader_callback_loader
#     def user_loader_callback(identity):
#         return User.query.filter((User.username == identity)).first()

#     @jwt.unauthorized_loader
#     def jwt_unauthorized_callback(self):
#         response = {
#             'error': {
#                 'message': 'Your auth token or CSRF token are missing'
#             }
#         }

#         return jsonify(response), 401

#     @jwt.expired_token_loader
#     def jwt_expired_token_callback():
#         response = {
#             'error': {
#                 'message': 'Your auth token has expired'
#             }
#         }

#         return jsonify(response), 401

#     return None

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)