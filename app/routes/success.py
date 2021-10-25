from flask_restful import Resource
import os
import time
import psutil

p = psutil.Process(os.getpid())

class Success(Resource):
    @classmethod
    def get(cls):
        """
        main route, lets admin know app is up
        """
        uptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))
        return {"status": "up", "uptime": uptime}, 200
