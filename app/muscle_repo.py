from sql.muscle_sql import *
from psycopg2 import IntegrityError
from app.utils import cursor_factory
from fastapi import HTTPException
from http.client import CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND


def create_muscle(muscle_data: dict):
    """
    Create a new muscle in the database.

    Args:
        muscle_data (dict): A dictionary containing muscle information.

    Returns:
        int: The ID of the created muscle.
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_MUSCLE,
                (
                    muscle_data["user_id"],
                    muscle_data["group_name"],
                    muscle_data["muscle_name"],
                    muscle_data["active"],
                ),
            )
            muscle_id = cursor.fetchone()[0]
            if not muscle_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to create muscle"
                )
            return muscle_id
        except IntegrityError as e:
            raise HTTPException(CONFLICT, detail="Muscle already exists") from e


def update_muscle(muscle_id: int, user_id: int, updates: dict):
    """
    Update an existing muscle in the database.

    Args:
        muscle_id (int): The ID of the muscle to update.
        user_id (int): The ID of the user who owns the muscle.
        updates (dict): A dictionary containing the updated muscle information.

    Returns:
        int: The ID of the updated muscle.
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                UPDATE_MUSCLE,
                (
                    updates["group_name"],
                    updates["muscle_name"],
                    updates["active"],
                    muscle_id,
                    user_id,
                ),
            )
            updated_id = cursor.fetchone()[0]
            if not updated_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to update muscle"
                )
            return updated_id
        except IntegrityError as e:
            raise HTTPException(
                CONFLICT, detail="Muscle update conflicts with existing data"
            ) from e


def get_default_muscles():
    """
    Retrieve all default muscles (system-defined muscles).

    Returns:
        list: A list of dictionaries containing muscle information.
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_DEFAULT_MUSCLES)
        muscles = cursor.fetchall()
        if not muscles:
            return []
        return [
            {
                "muscle_id": muscle[0],
                "user_id": muscle[1],
                "group_name": muscle[2],
                "muscle_name": muscle[3],
                "active": muscle[4],
            }
            for muscle in muscles
        ]


def get_all_muscles_by_user(user_id: int, limit: int = 50, offset: int = 0):
    """
    Retrieve all muscles for a specific user.

    Args:
        user_id (int): The ID of the user whose muscles to retrieve.
        limit (int): Maximum number of records to return.
        offset (int): Number of records to skip.

    Returns:
        list: A list of dictionaries containing muscle information.
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_ALL_MUSCLES_BY_USER, (user_id, limit, offset))
        muscles = cursor.fetchall()
        if not muscles:
            return []
        return [
            {
                "muscle_id": muscle[0],
                "user_id": muscle[1],
                "group_name": muscle[2],
                "muscle_name": muscle[3],
                "active": muscle[4],
            }
            for muscle in muscles
        ]


def delete_muscle(muscle_id: int, user_id: int):
    """
    Delete a muscle from the database.

    Args:
        muscle_id (int): The ID of the muscle to delete.
        user_id (int): The ID of the user who owns the muscle.

    Returns:
        int: The ID of the deleted muscle.
    """
    with cursor_factory() as cursor:
        cursor.execute(DELETE_MUSCLE, (muscle_id, user_id))
        deleted_id = cursor.fetchone()[0]
        if not deleted_id:
            raise HTTPException(NOT_FOUND, detail="Muscle not found")
        return deleted_id


def get_muscle_by_id(muscle_id: int, user_id: int):
    """
    Retrieve a muscle by its ID.

    Args:
        muscle_id (int): The ID of the muscle to retrieve
        user_id (int): The ID of the user who owns the muscle

    Returns:
        dict: A dictionary containing muscle information

    Raises:
        HTTPException: If muscle is not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_MUSCLE_BY_ID, (muscle_id, user_id))
        muscle = cursor.fetchone()
        if not muscle:
            raise HTTPException(NOT_FOUND, detail="Muscle not found")
        return {
            "muscle_id": muscle[0],
            "user_id": muscle[1],
            "group_name": muscle[2],
            "muscle_name": muscle[3],
            "active": muscle[4],
        }


def get_muscle_by_name(muscle_name: str, user_id: int):
    """
    Retrieve a muscle by its name.

    Args:
        muscle_name (str): The name of the muscle to retrieve
        user_id (int): The ID of the user who owns the muscle

    Returns:
        dict: A dictionary containing muscle information

    Raises:
        HTTPException: If muscle is not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_MUSCLE_BY_NAME, (muscle_name, user_id))
        muscle = cursor.fetchone()
        if not muscle:
            raise HTTPException(NOT_FOUND, detail="Muscle not found")
        return {
            "muscle_id": muscle[0],
            "user_id": muscle[1],
            "group_name": muscle[2],
            "muscle_name": muscle[3],
            "active": muscle[4],
        }
