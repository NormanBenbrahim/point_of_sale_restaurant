import traceback
import logging
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from app.extensions import db, jwt, marshmallow
from app.routes.success import Success
from app.routes.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from app.routes.menu import Menu, MenuList, MenuItem
from app.extensions import BLOCKLIST


# setup logger
logging.basicConfig(level=logging.INFO, # change to info in prod, add this to config later
                    format=f'%(asctime)s [%(levelname)s] %(pathname)s (line %(lineno)d) : %(message)s')


def create_app(settings_override=None):
    """
    create app function for dockerfile entry
    """
    try:
        # initialize app & define config scopes
        app = Flask(__name__, instance_relative_config=True)
        app.logger.info("Initializing app")

        # useful when hooking up the api to a front end or custom ajax later
        app.logger.info("Adding CORS")
        CORS(app)

        app.logger.info("Loading settings from config file")
        app.config.from_object('config.settings')
        app.config.from_pyfile('settings.py', silent=True)

        if settings_override:
            app.config.update(settings_override)

        # add extensions
        app.logger.info("Loading extensions")
        extensions(app)
        
        # make api
        app.logger.info("Loading restful interface")
        api = Api(app)

        # create tables
        app.logger.info("Creating database tables")
        @app.before_first_request
        def create_tables():
            db.create_all()

        # check if token blocklisted, best to use redis but sadly i couldn't get it to work
        #app.logger.info("Loading blocklisted tokens")
        #@jwt.token_in_blocklist_loader
        #def check_if_blocklist(token):
        #    return token['jti'] in BLOCKLIST

        # add routes, '/' first is best practice
        app.logger.info("Loading restful routes")
        api.add_resource(Success, app.config['ROUTE_SUCCESS'])

        # user routes
        api.add_resource(UserLogin, app.config['ROUTE_LOGIN'])
        api.add_resource(UserRegister, app.config['ROUTE_USER_REGISTER'])
        api.add_resource(User, app.config['ROUTE_USER'])
        api.add_resource(UserLogout, app.config['ROUTE_LOGOUT'])
        api.add_resource(TokenRefresh, app.config['ROUTE_REFRESH'])

        # menu routes
        api.add_resource(Menu, app.config['ROUTE_MENU'])
        api.add_resource(MenuList, app.config['ROUTE_MENU_LIST'])

        # orders route


        app.logger.info("API ready")
        return app

    # base exception to catch everything
    except BaseException:
        app.logger.error(f"There was an error: {traceback.format_exc()}")


def extensions(app):
    """
    register each loaded extension to the app, keep dir structure clean
    """
    jwt.init_app(app)
    db.init_app(app)
    marshmallow.init_app(app)

    return None 


if __name__ == '__main__':
    try:
        app = create_app()
        app.run(port=8080, debug=True)

    except BaseException:
        print(f"There was an error while creating the application: \n" + traceback.format_exc())