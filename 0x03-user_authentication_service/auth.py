#!/usr/bin/env python3
"""Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    Args:
        password (str): the password to hash
    Returns:
        bytes: a salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
