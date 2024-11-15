#!/usr/bin/env python3
"""
Module with class Auth
"""
import fnmatch
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require auth.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Normalize paths to ensure they end with a slash
        path = path.rstrip('/') + '/'
        excluded_paths = [p.rstrip('/') + '/' for p in excluded_paths]

        # Check for paths with '*' at the end
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Use fnmatch to match paths with the wildcard
                if fnmatch.fnmatch(path, excluded_path):
                    return False
            else:
                # Check for exact match
                if path == excluded_path:
                    return False

        # If no match, authentication is required
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization header, None, if not present.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authorization header from the request.
        Currently returns None.

        Args:
            request: The Flask request object.

        Returns:
            str: None, as the implementation is incomplete.
        """
        return None
