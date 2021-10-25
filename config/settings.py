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


#### common error messages
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."


##### database
db_uri = 'postgresql://{0}:{1}@postgres:5432/{2}'.format(os.environ['POSTGRES_USER'],
                                                         os.environ['POSTGRES_PASSWORD'],
                                                         os.environ['POSTGRES_DB'])
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

SEED_USER_EMAIL = 'dev@local.host'
SEED_USER_USERNAME = 'dev'
SEED_USER_PASSWORD = 'password'


##### json web token
JWT_TOKEN_LOCATION = ['cookies', 'headers'] # allow other clients to access
JWT_COOKIE_SECURE = False # change to true in production
JWT_SESSION_COOKIE = False # ccookies persist even after client is closed
JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=52) # token expiry 
JWT_ACCESS_COOKIE_PATH = '/'
JWT_COOKIE_CSRF_PROTECT = True # enable CSRF double submit protection 
