#!/usr/bin/env python3
"""Module that interacts with web server running on
http://localhost:5000. The web-server exposes/tests several
endpoints for user authentication and profile management"""

import requests

BASE_URL = 'http://localhost:5000'

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register a new user with the provided email and password"""

    url = f'{BASE_URL}/users'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json()['message'] == f'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the provided email and wrong password"""

    url = f'{BASE_URL}/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with the provided email and password"""

    url = f'{BASE_URL}/sessions'
    response = requests.post(url, data={'email': email, 'password': password})
    assert response.status_code == 200
    return response.json()['message']


def profile_unlogged() -> None:
    """Access the profile page without logging in."""

    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access the profile page while logged in"""

    url = f'{BASE_URL}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Log out the user with the provided session ID"""

    url = f'{BASE_URL}/sessions'
    headers = {'session_id': session_id}
    response = requests.delete(url, headers=headers)
    print(response.json())
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Generate reset password token for user with provided email"""

    url = f'{BASE_URL}/reset_password_token'
    response = requests.post(url, data={'email': email})
    assert response.status_code == 200
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password for user with the provided email and reset token"""

    url = f'{BASE_URL}/reset_password'
    response = requests.put(url,
                            data={'email': email, 'reset_token': reset_token,
                                  'new_password': new_password})
    assert response.status_code == 200
    assert response.json()['message'] == 'Password updated'


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
