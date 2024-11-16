#!/usr/bin/env python3
"""Session authentication module."""
from api.v1.auth.auth import Auth
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
