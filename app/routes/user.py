from flask_restful import Resource
from flask import request, current_app
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.extensions import app_error


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
        POST {current_app.config['ROUTE_USER_REGISTER']}
        """
        try:
            msg = f"POST Call to {current_app.config['ROUTE_USER_REGISTER']}"
            current_app.logger.info(msg)

            # define session
            _msg = "Defining session and passing to the load session"
            current_app.logger.info(_msg)
            session = scoped_session(sessionmaker(bind=engine))
            user = schema.load(request.get_json(), session=session)

            # handle duplicate users
            current_app.logger.info("Checking if user is duplicate")
            if UserModel.find_by_username(user.username):
                msg = current_app.config['MSG_USER_ALREADY_EXISTS']
                current_app.logger.warning(msg)
                return {"message": msg}, 400

            # add new user to database
            current_app.logger.info("Saving user to database")
            UserModel.save_to_db(user)

            current_app.logger.info(f"Successfully added {user}")
            out = {"message": current_app.config['MSG_CREATED_SUCCESSFULLY']}
            return out, 201

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()


class User(Resource):
    """
    restful interface for querying user info
    """
    @classmethod
    def get(cls, user_id: int):
        f"""
        route to look up a user

        postman request:
        GET {current_app.config['ROUTE_USER']}
        """
        try:
            msg = f"GET Call to route {current_app.config['ROUTE_USER']}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking or user in database")
            user = UserModel.find_by_id(user_id)

            # handle user not exist
            out = {"message": current_app.config['MSG_USER_NOT_FOUND']}
            if not user:
                current_app.logger.warning(out)
                return out, 404

            msg = f"User '{user.username}' in '{UserModel.__tablename__}' \
                database"
            current_app.logger.info(msg)
            return schema.dump(user), 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()

    @classmethod
    def delete(cls, user_id: int):
        f"""
        route to delete a user

        postman request:
        DELETE {current_app.config['ROUTE_USER']}
        """
        try:
            msg = f"DELETE Call to route {current_app.config['ROUTE_USER']}"
            current_app.logger.info(msg)

            current_app.logger.info("Looking for user")
            user = UserModel.find_by_id(user_id)

            # handle user not exist
            if not user:
                current_app.logger.warning(f"User {user.username} \
                    not found, caught error")

                out = {"message": current_app.config['MSG_USER_NOT_FOUND']}
                return out, 404

            # delete user
            current_app.logger.info("Deleting user")
            user.delete_from_db()

            current_app.logger.info(f"Successfully deleted {user.username}")
            return {"message": current_app.config['MSG_USER_DELETED']}, 200

        except BaseException:
            current_app.logger.error(app_error(nondict=True))
            return app_error()
