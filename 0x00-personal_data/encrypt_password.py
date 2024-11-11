#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    # Generate a salt with the default number of rounds (12)
    salt = bcrypt.gensalt(rounds=12)

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
