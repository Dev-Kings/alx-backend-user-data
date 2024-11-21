#!/usr/bin/env python3
"""Auth module
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        Args:
            email (str): the user's email
            password (str): the user's password
        Returns:
            User: the new User object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided password matches the hashed password in the db.
        Args:
            email (str): the user's email
            password (str): the user's password
        Returns:
            bool: True if the password is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    Args:
        password (str): the password to hash
    Returns:
        bytes: a salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid(self) -> str:
    """
    Generates and returns a new UUID as a string.
    """
    return str(uuid.uuid4())
