#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for storing session data in the database
    """

    def create_session(self, user_id=None):
        """
        Create and store a new UserSession
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Create a new UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the User ID based on session_id from UserSession
        """
        if session_id is None:
            return None

        all_sessions = UserSession.all()  # Retrieve all stored sessions
        user_session = None
        for session in all_sessions:
            if session.session_id == session_id:
                user_session = session
                break

        if user_session is None:
            # print("No matching session found")
            return None

        # Check session duration
        if self.session_duration <= 0:
            return user_session.user_id

        # Verify session expiration
        expiration_time = user_session.created_at + timedelta(
            seconds=self.session_duration)
        if expiration_time < datetime.now():
            # print("Session expired")
            return None

        print(f"Session valid for user_id: {user_session.user_id}")
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a UserSession based on the request cookie
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Find and delete session from the database
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
