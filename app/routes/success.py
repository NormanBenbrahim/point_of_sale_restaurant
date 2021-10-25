from flask_restful import Resource
from flask import current_app
import os
import time
import psutil

p = psutil.Process(os.getpid())

class Success(Resource):
    """
    restful(ish) interface to see if api is up
    """
    @classmethod
    def get(cls):
        f"""
        main route, lets admin know app is up

        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_SUCCESS']}
        """
        current_app.logger.info(f"Call to route {current_app.config['ROUTE_SUCCESS']}")
        
        uptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))
        current_app.logger.info(f"Uptime is {uptime}")
        
        return {"status": "up", "uptime": uptime}, 200
