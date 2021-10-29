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
ROUTE_MENU = '/menu/<int:menu_id>'
ROUTE_MENU_LIST = '/allmenus'
ROUTE_MENU_ITEM = '/menu/<int:menu_id>/<int:item_id>'
ROUTE_MENU_ITEM_LIST = '/menu/<int:menu_id>/allitems'


#### common messages
MSG_USER_ALREADY_EXISTS = "A user with that username already exists"
MSG_CREATED_SUCCESSFULLY = "User created successfully"
MSG_USER_NOT_FOUND = "User not found."
MSG_USER_DELETED = "User deleted"
MSG_INVALID_CREDENTIALS = "Invalid credentials!"
MSG_USER_LOGGED_OUT = "User successfully logged out"
MSG_MENU_ALREADY_EXISTS = "An item with name '{}' already exists"
MSG_ERROR_INSERTING = "An error occurred while inserting the menu"
MSG_MENU_NOT_FOUND = "Menu not found"
MSG_MENU_ITEM_NOT_FOUND = "Menu items not found"
MSG_MENU_FOUND = "Menu found"
MSG_MENU_DELETED = "Menu deleted"
MSG_MENU_ADDED = "Menu added"
MSG_MENU_UPDATED = "Menu updated"
MSG_MENU_INPUT_EMPTY = "No menu given"


##### databases
db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'
# bindkeys
USERS = 'users'
MENUS = 'menus'
# root url (users)
SQLALCHEMY_DATABASE_URI = db_uri.format(os.environ['POSTGRES_USER'],
                                        os.environ['POSTGRES_PASSWORD'],
                                        os.environ['POSTGRES_DB'])
# SQLALCHEMY_BINDS = {
#     MENUS: db_uri.format(os.environ['POSTGRES_USER'],
#                         os.environ['POSTGRES_PASSWORD'],
#                         os.environ['POSTGRES_DB_MENU'])
# }