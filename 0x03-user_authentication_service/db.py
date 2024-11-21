#!/usr/bin/env python3
"""DB module for the User class
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class for the User class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.
        Args:
            email (str): the user's email
            hashed_password (str): the user's hashed password

        Returns:
            User: The new User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)  # Refresh to get the auto-generated ID
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Get a user from the database
        Args:
            kwargs (dict): A dictionary of attributes to search for

        Returns:
            User: The first row that matches the search criteria
        Raises:
            - NoResultFound: If no results are found
            - InvalidRequestError: If the query is invalid
        """
        if not kwargs:
            raise InvalidRequestError("Invalid search criteria")
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found for the given criteria")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid search criteria")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database
        Args:
            user_id (int): The user ID
            kwargs (dict): A dictionary of attributes to update

        Returns:
            None
        Raises:
            ValueError: If user_id is not found
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("Invalid attribute: {}".format(key))
            setattr(user, key, value)
        self._session.commit()
        return None
