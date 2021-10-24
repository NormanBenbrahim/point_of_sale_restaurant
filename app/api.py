import traceback
from flask import Flask, jsonify
#from flask_jwt_extended import current_user

from app.extensions import debug_toolbar, db, jwt, marshmallow
from app.routes.index import index_route
from app.routes.menu import menu_route
from app.routes.orders import orders_route
from app.routes.healthcheck import healthcheck_route


def create_app(settings_override=None):
    """
    create app

    returns: flask app
    """
    try:
        app = Flask(__name__, instance_relative_config=True)

        app.config.from_object('config.settings')
        app.config.from_pyfile('settings.py', silent=True)

        if settings_override:
            app.config.update(settings_override)

        # add extensions
        extensions(app)

        # add routes, index should always go first
        app.register_blueprint(index_route)
        app.register_blueprint(healthcheck_route)
        app.register_blueprint(menu_route)
        app.register_blueprint(orders_route)

        return app

    except BaseException:
        print("There was an error while creating the application: \n" + traceback.format_exc())



def extensions(app):
    """
    register each loaded extension to the app

    app: flask app
    
    return: None
    """
    debug_toolbar.init_app(app)
    #jwt.init_app(app)
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
