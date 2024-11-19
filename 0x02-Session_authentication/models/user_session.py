#!/usr/bin/env python3
"""
UserSession module
"""

from typing import List
from models.base import Base


class UserSession(Base):
    """
    UserSession class for managing user sessions in a persistence layer
    """

    def __init__(self, *args: List, **kwargs: dict):
        """
        Constructor for UserSession class
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
