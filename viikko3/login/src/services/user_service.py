import string

from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")
        
        if not password_confirmation:
            raise UserInputError("Password confirmation required")
        
        if password != password_confirmation:
            raise UserInputError("Password and password confirmation don't match")
        
        if len(username) < 3:
            raise UserInputError("Username is too short")
        
        if len(password) < 8:
            raise UserInputError("Password is too short")
        
        letters = set(string.ascii_letters + "åäöÅÄÖ")
        non_letters = 0
        for letter in password:
            if letter not in letters:
                non_letters += 1

        if non_letters == 0:
            raise UserInputError("Password doesn't contain " + 
                                 "symbols outside of letters")

user_service = UserService()
