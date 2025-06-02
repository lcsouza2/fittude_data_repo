from sql.user_sql import *
from app.utils import cursor_factory
from psycopg2.errors import IntegrityError
from fastapi import HTTPException
from http.client import CONFLICT, INTERNAL_SERVER_ERROR
from pydantic import EmailStr


def create_user(user_data) -> bool:
    """
    Create a new user in the database.

    Args:
        user_data (dict): A dictionary containing user information.

    Returns:
        bool: True if the user was created successfully, False otherwise.

    Raises:
        HTTPException: If the user already exists or if the creation fails.
    """

    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_USER,
                user_data["email"],
                user_data["name"],
                user_data["password"],
            )

            created_id = cursor.fetchone()[0]

            if not created_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to create user"
                )
            return True
        except IntegrityError as e:
            raise HTTPException(CONFLICT, detail="User already exists") from e


def change_user_password(email: EmailStr, new_password: EmailStr) -> bool:
    """
    Change the password of an existing user.

    Args:
        email (str): The email of the user whose password is to be changed.
        new_password (str): The new password for the user.

    Returns:
        bool: True if the password was changed successfully, False otherwise.

    Raises:
        HTTPException: If the user does not exist or if the update fails.
    """

    with cursor_factory() as cursor:
        try:
            cursor.execute(UPDATE_USER_PASSWORD, new_password, email)

            updated = cursor.fetchone()[0]

            if not updated:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to update user password"
                )
            return True
        except IntegrityError as e:
            raise HTTPException(CONFLICT, detail="User does not exist") from e


def get_user_by_email(email: EmailStr) -> dict:
    """
    Retrieve a user by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        dict: A dictionary containing user information if found, None otherwise.
    """

    with cursor_factory() as cursor:
        cursor.execute(GET_USER_BY_EMAIL, (email,))
        user = cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2],
                "password": user[3],
            }
        return None


def get_user_by_id(user_id: int) -> dict:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: A dictionary containing user information if found, None otherwise.
    """

    with cursor_factory() as cursor:
        cursor.execute(GET_USER_BY_ID, (user_id,))
        user = cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2],
                "password": user[3],
            }
        return None
