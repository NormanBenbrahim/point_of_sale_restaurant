from flask import Flask

from app.extensions import debug_toolbar


def create_app(settings_override=None):
    """
    create app

    returns: flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    @app.route('/')
    def index():
        """
        toy example
        """
        return {"instance": app.config['WHICHINSTANCE']}

    return app


def extensions(app):
    """
    register each loaded extension to the app

    app: flask app
    
    return: None
    """
    # useful for when adding front end later
    debug_toolbar.init_app(app)

    return None 
