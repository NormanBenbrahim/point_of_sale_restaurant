from flask import Blueprint, jsonify
import os
import time
import psutil

p = psutil.Process(os.getpid())

healthcheck_route = Blueprint('healthcheck-route', __name__)

@healthcheck_route.route('/healthcheck', methods=['GET'])
def healthcheck():
    """
    monitor the uptime for the api. psutil has a lot more system info, used that so 
    we can store even more info later (if time)
    """
    uptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))
    
    return jsonify({'uptime': uptime})