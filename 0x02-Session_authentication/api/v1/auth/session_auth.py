#!/usr/bin/env python3
"""Session authentication module."""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Session authentication class.
    """
    # Dictionary to store session IDs and their corresponding user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user ID.
        Args:
            user_id (str): User ID.
        Returns:
            str: Session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID based on the Session ID.
        Args:
            session_id (str): Session ID.
        Returns:
            str: User ID, or None if session_id is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID using .get() for safe dictionary access
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance based on the cookie value.
        Args:
            request (Request): Flask request object.
        Returns:
            User: User instance, or None if not found.
        """
        if request is None:
            return None

        # Retrieve the session ID from the session cookie
        session_id = self.session_cookie(request)

        # Get the user ID based on the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Retrieve the User instance from the database
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout.
        Args:
            request (Request): Flask request object.
        Returns:
            None
        """
        if request is None:
            return None

        # Retrieve the session ID from the session cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        # Get the user ID based on the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Delete the session ID from the dictionary
        del self.user_id_by_session_id[session_id]

        return True
