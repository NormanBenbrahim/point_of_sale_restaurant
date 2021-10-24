from flask import Blueprint, jsonify

index_route = Blueprint('index-route', __name__)

@index_route.route('/', methods=['GET'])
def index():
    """
    hit the main endpoint for the app
    """
    return jsonify({'response': 200})
