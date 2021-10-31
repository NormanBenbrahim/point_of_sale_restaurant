import traceback
from flask import current_app, request
from flask.json import JSONDecoder
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# app specific extensions, add to extensions method in app.py
db = SQLAlchemy()
ma = Marshmallow()


def app_error(nondict=False):
    """
    helper function to return traceback
    """
    if nondict:
        return f"There was an application error. traceback: {traceback.format_exc()}"
    
    return {"There was an application error. traceback: ": f"{traceback.format_exc()}"}, 400

def check_payload():
    current_app.logger.info("Checking if payload is empty")

    data = request.get_data().decode('utf-8')
    current_app.logger.info(f"Request data: {data}")

    if len(request.get_data()) < 1:
        msg = current_app.config['MSG_PAYLOAD_EMPTY']
        current_app.logger.warning(msg)
        return {"message": msg}, 404
    
    return None
