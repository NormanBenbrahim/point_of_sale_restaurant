from flask_restful import Resource
from flask import current_app
import os
import time
import psutil

from app.extensions import app_error


p = psutil.Process(os.getpid())


class Success(Resource):
    """
    restful interface to see if api is up
    """
    @classmethod
    def get(cls):
        f"""
        main route, lets admin know app is up

        postman request:
        GET {current_app.config['ROUTE_SUCCESS']}
        """
        try:
            msg = f"Call to route {current_app.config['ROUTE_SUCCESS']}"
            current_app.logger.info(msg)

            out = "%Y-%m-%d %H:%M:%S"
            uptime = time.strftime(out, time.localtime(p.create_time()))
            current_app.logger.info(f"Uptime is {uptime}")

            return {"status": "up", "uptime": uptime}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()
