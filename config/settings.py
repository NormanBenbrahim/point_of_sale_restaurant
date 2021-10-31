import os


##### helps to debug 
WHICHINSTANCE = "dev config"
DEBUG = True # in prod change this


##### cors
CORS_HEADER = 'Content-Type'


##### main url
SERVER_NAME = '0.0.0.0:8000'


##### endpoints for routes
ROUTE_SUCCESS =  '/'
ROUTE_USER_REGISTER = '/register'
ROUTE_USER = '/user/<int:user_id>'
ROUTE_LOGIN = '/login'
ROUTE_LOGOUT = '/logout'
ROUTE_REFRESH = '/refresh'
ROUTE_MENU = '/add-item'
ROUTE_MENU_ITEM = '/menu/<int:item_id>'
ROUTE_MENU_LIST = '/all-items'
ROUTE_ORDER = '/add-order'
ROUTE_ORDER_ITEM = '/order/<int:order_id>'
ROUTE_ORDER_LIST = '/all-orders'


#### common messages
MSG_USER_ALREADY_EXISTS = "A user with that username already exists"
MSG_CREATED_SUCCESSFULLY = "User created successfully"
MSG_USER_NOT_FOUND = "User not found."
MSG_USER_DELETED = "User deleted"
MSG_INVALID_CREDENTIALS = "Invalid credentials!"
MSG_USER_LOGGED_OUT = "User successfully logged out"
MSG_MENU_ALREADY_EXISTS = "A menu with name '{}' already exists"
MSG_ERROR_INSERTING = "An error occurred while inserting the menu"
MSG_ITEM_NOT_FOUND = "Item '{}' not found"
MSG_ITEM_EXISTS = "Item with id '{}' already exists"
MSG_ITEM_DELETED = "Item with id '{}' deleted"
MSG_ORDER_EXISTS = "Order with id '{}' already exists"
MSG_VALIDATION_ERROR = "There was an error in your payload input: {}"


##### databases
db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'
# root url (users)
SQLALCHEMY_DATABASE_URI = db_uri.format(os.environ['POSTGRES_USER'],
                                        os.environ['POSTGRES_PASSWORD'],
                                        os.environ['POSTGRES_DB'])

SQLALCHEMY_TRACK_MODIFICATIONS = False