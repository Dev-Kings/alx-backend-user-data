#!/usr/bin/env python3
"""
Module with class Auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path.
        For now, always returns False.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require auth.

        Returns:
            bool: False, as the implementation is incomplete.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request.
        Currently returns None.

        Args:
            request: The Flask request object.

        Returns:
            str: None, as the implementation is incomplete.

        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authorization header from the request.
        Currently returns None.

        Args:
            request: The Flask request object.

        Returns:
            str: None, as the implementation is incomplete.
        """
        return None
