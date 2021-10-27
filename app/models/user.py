from app.extensions import db
from flask import current_app

class UserModel(db.Model):
    """
    main model for our userbase, errors are handled in user routes
    """
    __tablename__ = "users_table"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        """
        utility to search for a user, see routes for usage
        """
        current_app.logger.info("find_by_username subroutine called")
        
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        """
        utility to search for user, see routes for usage
        """
        current_app.logger.info("find_by_id subroutine called")
        
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self) -> None:
        """
        save user to the database
        """
        current_app.logger.info("Adding user to database")
        
        db.session.add(self)
        db.session.commit()

        current_app.logger.info("Successfully added user")


    def delete_from_db(self) -> None:
        """
        delete user from the database
        """
        current_app.logger.info("Deleting user from database")

        db.session.delete(self)
        db.session.commit()

        current_app.logger.info("Successfully deleted user")
