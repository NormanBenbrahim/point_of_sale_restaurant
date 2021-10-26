from datetime import timedelta 
import os 

##### helps to debug 
WHICHINSTANCE = "dev config"
DEBUG = True # in prod change this

##### where to log
LOG_DIR = "app/logs"

##### main url
SERVER_NAME = '0.0.0.0:8000'


##### endpoints for routes
ROUTE_SUCCESS =  '/'
ROUTE_USER_REGISTER = '/register'
ROUTE_USER = '/user/<int:user_id>'
ROUTE_LOGIN = '/login'
ROUTE_LOGOUT = '/logout'
ROUTE_REFRESH = '/refresh'


#### common messages
MSG_USER_ALREADY_EXISTS = "A user with that username already exists."
MSG_CREATED_SUCCESSFULLY = "User created successfully."
MSG_USER_NOT_FOUND = "User not found."
MSG_USER_DELETED = "User deleted."
MSG_INVALID_CREDENTIALS = "Invalid credentials!"
MSG_USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."


##### database
db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'.format(os.environ['POSTGRES_USER'],
                                                         os.environ['POSTGRES_PASSWORD'],
                                                         os.environ['POSTGRES_DB'])
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False


##### jwt settings, chose to use HS* algorithm as it's easier to implement
JWT_TOKEN_LOCATION = ['cookies', 'headers'] # allow other clients to access
JWT_SECRET_KEY = os.urandom(16) # initialize api's secret key for HS* algorithm
JWT_COOKIE_SECURE = True # change to true in production
JWT_SESSION_COOKIE = True # ccookies persist even after client is closed
JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=52) # token expiry 
JWT_ACCESS_COOKIE_PATH = '/'
JWT_COOKIE_CSRF_PROTECT = True # enable CSRF double submit protection 
