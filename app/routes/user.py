from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from marshmallow import ValidationError

from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.extensions import BLOCKLIST


# initialize the schema for users
schema = UserSchema()


class UserRegister(Resource):
    """
    restful interface for registering new users
    """
    @classmethod
    def post(cls):
        f"""
        route to create new user in the database
        
        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER_REGISTER']}
        """
        try:
            current_app.logger.info(f"POST Call to route {current_app.config['ROUTE_USER_REGISTER']}")

            # define session
            current_app.logger.info(f"Defining session and passing to the load session")
            session = scoped_session(sessionmaker(bind=engine))
            user = schema.load(request.get_json(), session=session)

            # handle duplicate users
            current_app.logger.info("Checking if user is duplicate")
            if UserModel.find_by_username(user.username):
                current_app.logger.warning(f"Duplicate user caught for {user.username}, didn't create")
                return {"message": current_app.config['MSG_USER_ALREADY_EXISTS']}, 400
            
            # add new user to database
            current_app.logger.info("Saving user to database")
            UserModel.save_to_db(user)

            current_app.logger.info(f"Successfully added {user}")
            return {"message": current_app.config['MSG_CREATED_SUCCESSFULLY']}, 201

        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")


class User(Resource):
    """
    restful interface for querying user info
    """
    @classmethod
    def get(cls, user_id: int):
        f"""
        route to look up a user
        
        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER']}
        """
        try:
            current_app.logger.info(f"GET Call to route {current_app.config['ROUTE_USER']}")

            current_app.logger.info("Looking or user in database")
            user = UserModel.find_by_id(user_id)

            # handle user not exist
            if not user:
                current_app.logger.warning(f"User {user.username} not found, caught error")
                return {"message": current_app.config['MSG_USER_NOT_FOUND']}, 404

            current_app.logger.info(f"User '{user.username}' in '{UserModel.__tablename__}' database")
            return schema.dump(user), 200

        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")

    
    @classmethod
    def delete(cls, user_id: int):
        f"""
        route to delete a user
        
        postman request:
        DELETE {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER']}
        """
        try:
            current_app.logger.info(f"DELETE Call to route {current_app.config['ROUTE_USER']}")

            current_app.logger.info("Looking for user")
            user = UserModel.find_by_id(user_id)

            # handle user not exist
            if not user:
                current_app.logger.warning(f"User {user.username} not found, caught error")
                return{"message": current_app.config['MSG_USER_NOT_FOUND']}, 404

            # delete user
            current_app.logger.info("Deleting user")
            user.delete_from_db()

            current_app.logger.info(f"Successfully deleted {user.username}")
            return {"message": current_app.config['MSG_USER_DELETED']}, 200

        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")


class UserLogin(Resource):
    """
    restful interface for login 
    """
    @classmethod
    def post(cls):
        f"""
        route to login safely with jwt tokens

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_LOGIN']}
        """
        try:
            current_app.logger.info(f"POST call to route {current_app.config['ROUTE_LOGIN']}")
            # handle user not exist separately to not break the code 
            try:
                current_app.logger.info("Loading user schema from web token")

                # define session
                current_app.logger.info(f"Defining session and passing to the load session")
                session = scoped_session(sessionmaker(bind=engine))
                user_data = schema.load(request.get_json(), session=session)
            
            except ValidationError as err:
                current_app.logger.warning("Loading user schema")
                return err.messages, 400

            # load user
            current_app.logger.info(f"Loading user")
            user = UserModel.find_by_username(user_data.username)

            # handle passwords securely & give user their tokens
            current_app.logger.info(f"Creating user tokens")
            if user and safe_str_cmp(user_data.password, user.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                
                current_app.logger.info(f"User '{user_data.username}' logged in")
                return {"access_token": access_token, "refresh_token": refresh_token}, 200

            # bad/no tokens
            return {"message": current_app.config['MSG_INVALID_CREDENTIALS']}, 401
        
        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")


class UserLogout(Resource):
    """
    restful interface for user logout
    """
    @classmethod
    @jwt_required
    def post(cls):
        f"""
        route to logout safely and add their token to blocklist, couldn't get redis to work
        so chose to store in extensions

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_LOGOUT']}        
        """
        try:
            current_app.logger.info(f"POST call to route {current_app.config['ROUTE_LOGOUT']}")
            
            # get current json web token and add to blocklist
            current_app.logger.info("Adding current user token to blocklist")
            jti = get_jwt()['jti']
            user_id = get_jwt_identity()
            BLOCKLIST.add(jti)
            
            # next request with the token won't work
            current_app.logger.info("User logged out")
            return {"message": current_app.config['MSG_USER_LOGGED_OUT'].format(user_id)}, 200

        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")


class TokenRefresh(Resource):
    """
    restful interface for refreshing json web tokens
    """
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        f"""
        route to refresh json web tokens

        postman request:
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_REFRESH']} 
        
        HEADERS
        KEY=Authorization 
        VALUE=Bearer <token>
        """
        try:
            current_app.logger.info(f"POST call to route {current_app.config['ROUTE_REFRESH']}")

            current_app.logger.info(f"Creating new user token")
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            
            current_app.logger.info("Token refreshed")
            return {"access_token": new_token}, 200

        except BaseException as err:
            current_app.logger.error(f"There was an {err} error")
