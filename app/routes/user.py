from flask_restful import Resource
from flask import request, current_app
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
        route to create new user in the database, config contains routenames
        
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER_REGISTER']}
        """
        # handle bad requests
        try:
            user = schema.load(request)
        
        except ValidationError as err:
            return err.messages, 400

        # handle duplicate users
        if UserModel.find_by_username(user.username):
            return {"message": current_app.config['USER_ALREADY_EXISTS']}, 400
        
        # add new user to database
        user.save_to_db()

        return {"message": current_app.config['CREATED_SUCCESSFULLY']}, 201


class User(Resource):
    """
    restful interface for querying user info
    """
    @classmethod
    def get(cls, user_id: int):
        f"""
        route to look up a user, config contains routenames
        
        postman request:
        GET {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER']}
        """
        user = UserModel.find_by_id(user_id)

        # handle user not exist
        if not user:
            return {"message": current_app.config['USER_NOT_FOUND']}, 404

        return schema.dump(user), 200

    
    @classmethod
    def delete(cls, user_id: int):
        f"""
        route to delete a user
        
        postman request:
        DELETE {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_USER']}
        """
        user = UserModel.find_by_id(user_id)

        # handle user not exist
        if not user:
            return{"message": current_app.config['USER_NOT_FOUND']}, 404

        # delete user
        user.delete_from_db()

        return {"message": current_app.config['USER_DELETED']}, 200


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
        # handle user not exist
        try:
            user_json = request.get_json()
            user_data = schema.load(user_json)
        
        except ValidationError as err:
            return err.messages, 400

        # load user
        user = UserModel.find_by_username(user_data.username)

        # handle passwords securely & give user their tokens
        if user and safe_str_cmp(user_data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        # bad/no tokens
        return {"message": current_app.config['INVALID_CREDENTIALS']}, 401


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
        POST {current_app.config['SERVER_NAME']}{current_app.config['ROUTE_LOGIN']}        
        """
        # get current json web token and add to blocklist
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        
        # next request with the token won't work
        return {"message": current_app.config['USER_LOGGED_OUT'].format(user_id)}, 200   


class TokenRefresh(Resource):
    """
    restful interface for refreshing json web tokens
    """
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        """
        utility to refresh json web tokens
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        return {"access_token": new_token}, 200
