from flask import Blueprint 

index_route = Blueprint('index-route', __name__)

@index_route.route('/', methods=['GET'])
def index():
    return {'response': 200}
