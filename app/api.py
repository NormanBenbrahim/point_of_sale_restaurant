import logging
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from app.extensions import db, ma, app_error
from app.routes.success import Success
from app.routes.user import UserRegister, User
from app.routes.menu import (
    MenuAdd,
    MenuItem,
    MenuList,
    OrderAdd,
    OrderList,
    OrderItem
)

# setup logger
format = "%(asctime)s [%(levelname)s] %(pathname)s \
    (line %(lineno)d) : %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=format)


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
        @app.before_first_request
        def create_tables():
            app.logger.info("Creating database tables")
            db.create_all()

        # add routes, '/' first is best practice
        app.logger.info("Loading restful routes")
        api.add_resource(Success, app.config['ROUTE_SUCCESS'])

        # user routes
        api.add_resource(UserRegister, app.config['ROUTE_USER_REGISTER'])
        api.add_resource(User, app.config['ROUTE_USER'])

        # menu routes
        api.add_resource(MenuAdd, app.config['ROUTE_MENU'])
        api.add_resource(MenuItem, app.config['ROUTE_MENU_ITEM'])
        api.add_resource(MenuList, app.config['ROUTE_MENU_LIST'])

        # order routes
        api.add_resource(OrderAdd, app.config['ROUTE_ORDER'])
        api.add_resource(OrderList, app.config['ROUTE_ORDER_LIST'])
        api.add_resource(OrderItem, app.config['ROUTE_ORDER_ITEM'])

        app.logger.info("API ready")
        return app

    # base exception to catch everything
    except BaseException:
        app.logger.error(app_error(nondict=True))
        return app_error()


def extensions(app):
    """
    register each loaded extension to the app, keep dir structure clean
    """
    db.init_app(app)
    ma.init_app(app)

    return None


if __name__ == '__main__':
    try:
        import os
        from dotenv import load_dotenv

        load_dotenv()

        POSTGRES_USER = os.environ['POSTGRES_USER']
        print("POSTGRES USER:" + POSTGRES_USER)
        POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
        POSTGRES_DB = os.environ['POSTGRES_DB']
        db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'.format(
            POSTGRES_USER,
            POSTGRES_PASSWORD,
            POSTGRES_DB
        )

        app = create_app()
        app.config['DATABASE_URL'] = db_uri
        app.run(port=5000, debug=True)

    except BaseException:
        print(app_error(nondict=True))
