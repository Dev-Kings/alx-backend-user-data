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

    def create_session(self, email: str) -> str:
        """
        Creates a session for the given user.
        Args:
            email (str): the user's email
        Returns:
            str: Session created.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()

            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session for a given user.
        Args:
            user_id (int): the user's id
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Gets a user from a session id.
        Args:
            session_id (str): the session id
        Returns:
            User: the user' queried, or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token.
        Args:
            email (str): the user's email
        Returns:
            str: the reset password token
        Raises:
            ValueError: if the user doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password.
        Args:
            reset_token (str): the reset token
            password (str): the new password
        Raises:
            ValueError: if the token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None
            )
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    Args:
        password (str): the password to hash
    Returns:
        bytes: a salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates and returns a new UUID as a string.
    """
    return str(uuid.uuid4())
