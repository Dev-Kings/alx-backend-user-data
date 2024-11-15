#!/usr/bin/env python3
"""
BasicAuth module for managing basic authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for
        Basic Authentication

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the header if valid, otherwise None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 string of the Authorization header

        Args:
            base64_authorization_header (str): The Base64 string

        Returns:
            str: The decoded value as UTF8 string, or None if invalid
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email and password from the Base64 decoded value

        Args:
            decoded_base64_authorization_header (str): Decoded Base64 value

        Returns:
            (str, str): Tuple of user email and password, or (None, None)
            if invalid
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Split the decoded string into email and password
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if found and authenticated, otherwise None.
        """
        # Validate inputs
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for the user in the database
            user_list = User.search({'email': user_email})

        except Exception:
            # If no user found with the provided email
            return None

        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
            else:
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request

        Args:
            request (Request): The request object

        Returns:
            User: The User instance if valid, otherwise None
        """
        # Extract the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract the Base64 part of the header
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        # Decode the Base64 string
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        # Extract the user credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the User instance
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
