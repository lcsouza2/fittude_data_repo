from sql.equipment_sql import *
from psycopg2 import IntegrityError
from app.utils import cursor_factory
from fastapi import HTTPException
from http.client import CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND


def create_equipment(equipment_data: dict):
    """
    Create a new equipment in the database.

    Args:
        equipment_data (dict): A dictionary containing equipment information.

    Returns:
        int: The ID of the created equipment.
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_EQUIPMENT,
                (
                    equipment_data["user_id"],
                    equipment_data["group_name"],
                    equipment_data["equipment_name"],
                    equipment_data["active"],
                ),
            )
            equipment_id = cursor.fetchone()[0]
            if not equipment_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to create equipment"
                )
            return equipment_id
        except IntegrityError as e:
            raise HTTPException(CONFLICT, detail="Equipment already exists") from e


def update_equipment(equipment_id: int, user_id: int, updates: dict):
    """
    Update an existing equipment in the database.

    Args:
        equipment_id (int): The ID of the equipment to update.
        user_id (int): The ID of the user who owns the equipment.
        updates (dict): A dictionary containing the updated equipment information.

    Returns:
        int: The ID of the updated equipment.
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                UPDATE_EQUIPMENT,
                (
                    updates["group_name"],
                    updates["equipment_name"],
                    updates["active"],
                    equipment_id,
                    user_id,
                ),
            )
            updated_id = cursor.fetchone()[0]
            if not updated_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to update equipment"
                )
            return updated_id
        except IntegrityError as e:
            raise HTTPException(
                CONFLICT, detail="Equipment update conflicts with existing data"
            ) from e


def get_equipment_by_id(equipment_id: int, user_id: int):
    """
    Retrieve an equipment by its ID.

    Args:
        equipment_id (int): The ID of the equipment to retrieve.
        user_id (int): The ID of the user who owns the equipment.

    Returns:
        dict: A dictionary containing equipment information if found, None otherwise.
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EQUIPMENT_BY_ID, (equipment_id, user_id))
        equipment = cursor.fetchone()
        if equipment:
            return {
                "equipment_id": equipment[0],
                "user_id": equipment[1],
                "group_name": equipment[2],
                "equipment_name": equipment[3],
                "active": equipment[4],
            }
        raise HTTPException(NOT_FOUND, detail="Equipment not found")


def get_equipment_by_name(equipment_name: str, user_id: int):
    """
    Retrieve an equipment by its name.

    Args:
        equipment_name (str): The name of the equipment to retrieve.
        user_id (int): The ID of the user who owns the equipment.

    Returns:
        dict: A dictionary containing equipment information if found, None otherwise.
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EQUIPMENT_BY_NAME, (equipment_name, user_id))
        equipment = cursor.fetchone()
        if equipment:
            return {
                "equipment_id": equipment[0],
                "user_id": equipment[1],
                "group_name": equipment[2],
                "equipment_name": equipment[3],
                "active": equipment[4],
            }
        raise HTTPException(NOT_FOUND, detail="Equipment not found")


def get_all_equipment_by_user(user_id: int, limit: int = 50, offset: int = 0):
    """
    Retrieve all equipment for a specific user.

    Args:
        user_id (int): The ID of the user whose equipment to retrieve.

    Returns:
        list: A list of dictionaries containing equipment information.
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_ALL_EQUIPMENT_BY_USER, (user_id, limit, offset))
        equipment_list = cursor.fetchall()
        if not equipment_list:
            raise HTTPException(NOT_FOUND, detail="No equipment found for this user")
        return [
            {
                "equipment_id": eq[0],
                "user_id": eq[1],
                "group_name": eq[2],
                "equipment_name": eq[3],
                "active": eq[4],
            }
            for eq in equipment_list
        ]


def delete_equipment(equipment_id: int, user_id: int):
    """
    Delete an equipment from the database.

    Args:
        equipment_id (int): The ID of the equipment to delete.
        user_id (int): The ID of the user who owns the equipment.

    Returns:
        int: The ID of the deleted equipment.
    """
    with cursor_factory() as cursor:
        cursor.execute(DELETE_EQUIPMENT, (equipment_id, user_id))
        deleted_id = cursor.fetchone()[0]
        if not deleted_id:
            raise HTTPException(NOT_FOUND, detail="Equipment not found")
        return deleted_id
