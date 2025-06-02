from sql.exercise_sql import *
from psycopg2 import IntegrityError
from app.utils import cursor_factory
from fastapi import HTTPException
from http.client import CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND


def create_exercise(exercise_data: dict) -> int:
    """
    Create a new exercise in the database.

    Args:
        exercise_data (dict): Dictionary containing exercise information

    Returns:
        int: ID of the created exercise

    Raises:
        HTTPException: If creation fails or exercise already exists
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_EXERCISE,
                (
                    exercise_data["user_id"],
                    exercise_data["exercise_name"],
                    exercise_data["description"],
                    exercise_data["active"],
                ),
            )
            exercise_id = cursor.fetchone()[0]
            if not exercise_id:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, detail="Failed to create exercise"
                )
            return exercise_id
        except IntegrityError as e:
            raise HTTPException(CONFLICT, detail="Exercise already exists") from e


def update_exercise(exercise_id: int, user_id: int, updates: dict) -> int:
    """
    Update an existing exercise.

    Args:
        exercise_id (int): ID of exercise to update
        user_id (int): ID of user who owns the exercise
        updates (dict): Dictionary containing fields to update

    Returns:
        int: ID of updated exercise

    Raises:
        HTTPException: If update fails or exercise not found
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                UPDATE_EXERCISE,
                (
                    updates["exercise_name"],
                    updates["description"],
                    updates["active"],
                    exercise_id,
                    user_id,
                ),
            )
            updated_id = cursor.fetchone()[0]
            if not updated_id:
                raise HTTPException(NOT_FOUND, detail="Exercise not found")
            return updated_id
        except IntegrityError as e:
            raise HTTPException(
                CONFLICT, detail="Exercise update conflicts with existing data"
            ) from e


def get_default_exercises() -> list:
    """
    Get all default (system) exercises.

    Returns:
        list: List of dictionaries containing exercise information
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_DEFAULT_EXERCISES)
        exercises = cursor.fetchall()
        return [
            {
                "exercise_id": ex[0],
                "user_id": ex[1],
                "exercise_name": ex[2],
                "description": ex[3],
                "active": ex[4],
            }
            for ex in exercises
        ]


def get_exercise_by_id(exercise_id: int, user_id: int) -> dict:
    """
    Get an exercise by its ID and user ID.

    Args:
        exercise_id (int): ID of the exercise to retrieve
        user_id (int): ID of the user who owns the exercise

    Returns:
        dict: Dictionary containing exercise information

    Raises:
        HTTPException: If exercise not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EXERCISE_BY_ID, (exercise_id, user_id))
        exercise = cursor.fetchone()
        if not exercise:
            raise HTTPException(NOT_FOUND, detail="Exercise not found")
        return {
            "exercise_id": exercise[0],
            "user_id": exercise[1],
            "exercise_name": exercise[2],
            "description": exercise[3],
            "active": exercise[4],
        }


def get_exercise_by_name(exercise_name: str, user_id: int) -> dict:
    """
    Get an exercise by its name and user ID.

    Args:
        exercise_name (str): Name of the exercise to retrieve
        user_id (int): ID of the user who owns the exercise

    Returns:
        dict: Dictionary containing exercise information

    Raises:
        HTTPException: If exercise not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EXERCISE_BY_NAME, (exercise_name, user_id))
        exercise = cursor.fetchone()
        if not exercise:
            raise HTTPException(NOT_FOUND, detail="Exercise not found")
        return {
            "exercise_id": exercise[0],
            "user_id": exercise[1],
            "exercise_name": exercise[2],
            "description": exercise[3],
            "active": exercise[4],
        }


def get_all_exercises_by_user(user_id: int, limit: int = 50, offset: int = 0) -> list:
    """
    Get all exercises for a specific user.

    Args:
        user_id (int): ID of user whose exercises to retrieve
        limit (int): Maximum number of exercises to return
        offset (int): Number of exercises to skip

    Returns:
        list: List of dictionaries containing exercise information
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_ALL_EXERCISES_BY_USER, (user_id, limit, offset))
        exercises = cursor.fetchall()
        return [
            {
                "exercise_id": ex[0],
                "user_id": ex[1],
                "exercise_name": ex[2],
                "description": ex[3],
                "active": ex[4],
            }
            for ex in exercises
        ]


def bind_muscle_to_exercise(exercise_id: int, muscle_id: int) -> int:
    """
    Associate a muscle with an exercise.

    Args:
        exercise_id (int): ID of the exercise
        muscle_id (int): ID of the muscle to bind

    Returns:
        int: ID of the exercise the muscle was bound to

    Raises:
        HTTPException: If binding fails or already exists
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(BIND_MUSCLE_TO_EXERCISE, (muscle_id, exercise_id))
            return cursor.fetchone()[0]
        except IntegrityError as e:
            raise HTTPException(
                CONFLICT, detail="Muscle already bound to exercise"
            ) from e


def bind_equipment_to_exercise(exercise_id: int, equipment_id: int) -> int:
    """
    Associate equipment with an exercise.

    Args:
        exercise_id (int): ID of the exercise
        equipment_id (int): ID of the equipment to bind

    Returns:
        int: ID of the exercise the equipment was bound to

    Raises:
        HTTPException: If binding fails or already exists
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(BIND_EQUIPMENT_TO_EXERCISE, (equipment_id, exercise_id))
            return cursor.fetchone()[0]
        except IntegrityError as e:
            raise HTTPException(
                CONFLICT, detail="Equipment already bound to exercise"
            ) from e


def get_exercise_muscles(exercise_id: int) -> list:
    """
    Get all muscles associated with an exercise.

    Args:
        exercise_id (int): ID of the exercise

    Returns:
        list: List of dictionaries containing muscle information
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EXERCISE_MUSCLES, (exercise_id,))
        muscles = cursor.fetchall()
        return [
            {"muscle_id": m[0], "muscle_name": m[1], "group_name": m[2]}
            for m in muscles
        ]


def get_exercise_equipment(exercise_id: int) -> list:
    """
    Get all equipment associated with an exercise.

    Args:
        exercise_id (int): ID of the exercise

    Returns:
        list: List of dictionaries containing equipment information
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_EXERCISE_EQUIPMENT, (exercise_id,))
        equipment = cursor.fetchall()
        return [
            {"equipment_id": e[0], "equipment_name": e[1], "group_name": e[2]}
            for e in equipment
        ]
