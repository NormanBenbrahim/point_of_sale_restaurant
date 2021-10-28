import traceback
from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError

from app.models.user import UserModel
from app.schemas.user import UserSchema


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

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")


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

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")

    
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

        except BaseException:
            current_app.logger.error(f"There was an error: {traceback.format_exc()}")
