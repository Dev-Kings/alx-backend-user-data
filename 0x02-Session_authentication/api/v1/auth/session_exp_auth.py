#!/usr/bin/env python3
"""SessionExpAuth module"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth inherits from SessionAuth
    Adds session expiration feature
    """

    def __init__(self):
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID and store session data
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Store session data with creation time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get user ID from session ID
        """
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if "user_id" not in session_dict or "created_at" not in session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(
            seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
