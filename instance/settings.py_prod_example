import os


# helps to debug
WHICHINSTANCE = "dev config"
DEBUG = True  # in prod change this


# cors
CORS_HEADER = 'Content-Type'


# main url
SERVER_NAME = '0.0.0.0:8000'


# endpoints for routes
ROUTE_SUCCESS = '/'
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


# common messages
PAYLOAD_EMPTY = 'No input provided'
USER_ALREADY_EXISTS = "A user with that username already exists"
CREATED_SUCCESSFULLY = "User created successfully"
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted"
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User successfully logged out"
MENU_ALREADY_EXISTS = "A menu with name '{}' already exists"
MENU_UPDATED = "Menu updated"
ORDER_UPDATED = "Order updated"
ERROR_INSERTING = "An error occurred while inserting the menu"
ITEM_NOT_FOUND = "Item '{}' not found"
ORDER_NOT_FOUND = "Order '{}' not found"
ORDER_ADDED = "Order '{}' added"
ORDER_DELETED = "Order with id '{}' deleted"
ITEM_EXISTS = "Item with id '{}' already exists"
ITEM_DELETED = "Item with id '{}' deleted"
ITEM_ADDED = "Item '{}' added"
ORDER_EXISTS = "Order with id '{}' already exists"
VALIDATION_ERROR = "There was an error in your payload input: {}"
ITEM_INSUFFICIENT = "Insufficient quantity for item with id {}, there are {} \
    available on the menu"
PAYMENT_INSUFFICIENT = "Payment insufficient. Total due: ${}, payment amount: ${}, \
    remaining amount due: ${}"
PAYMENT_OVERCHARGE = "Overcharging for order. Total due: ${}, payment_amount: ${}, \
    overcharged by: ${}"


# databases
db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'

# root url (users)
SQLALCHEMY_DATABASE_URI = db_uri.format(os.environ['POSTGRES_USER'],
                                        os.environ['POSTGRES_PASSWORD'],
                                        os.environ['POSTGRES_DB'])

SQLALCHEMY_TRACK_MODIFICATIONS = False
