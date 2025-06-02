from fastapi import HTTPException
from http import HTTPStatus
from psycopg2.errors import UniqueViolation
from typing import List
from utils import cursor_factory
from sql.workout_plan_sql import *


def create_workout_plan(user_id: int, plan_data: dict) -> bool:
    """
    Create a new workout plan for a user.

    Args:
        user_id (int): ID of the user creating the plan
        plan_data (dict): Workout plan data containing name and goal

    Returns:
        bool: True if workout plan was created successfully

    Raises:
        HTTPException: If plan with same name already exists
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_WORKOUT_PLAN,
                (
                    user_id,
                    plan_data["workout_plan_name"],
                    plan_data["workout_plan_goal"],
                    plan_data.get("active", True)
                )
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Failed to create workout plan"
                )
            return True
        except UniqueViolation:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                detail="Workout plan with this name already exists"
            )


def update_workout_plan(workout_plan_id: int, user_id: int, plan_data: dict) -> bool:
    """
    Update an existing workout plan.

    Args:
        workout_plan_id (int): ID of the workout plan to update
        user_id (int): ID of the user owning the plan
        plan_data (dict): Updated workout plan data

    Returns:
        bool: True if workout plan was updated successfully

    Raises:
        HTTPException: If plan not found or update fails
    """
    with cursor_factory() as cursor:
        cursor.execute(
            UPDATE_WORKOUT_PLAN,
            (
                plan_data["workout_plan_name"],
                plan_data["workout_plan_goal"],
                plan_data.get("active", True),
                workout_plan_id,
                user_id
            )
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to update workout plan"
            )
        return True


def get_workout_plan_by_id(workout_plan_id: int, user_id: int) -> dict:
    """
    Get a workout plan by its ID.

    Args:
        workout_plan_id (int): ID of the workout plan to retrieve
        user_id (int): ID of the user owning the plan

    Returns:
        dict: Workout plan information

    Raises:
        HTTPException: If plan not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_WORKOUT_PLAN_BY_ID, (workout_plan_id, user_id))
        plan = cursor.fetchone()
        if not plan:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Workout plan not found"
            )
        return {
            "workout_plan_id": plan[0],
            "user_id": plan[1],
            "workout_plan_name": plan[2],
            "workout_plan_goal": plan[3],
            "active": plan[4]
        }


def get_workout_plans_by_user(
    user_id: int,
    limit: int = 10,
    offset: int = 0
) -> List[dict]:
    """
    Get all workout plans for a user with pagination.

    Args:
        user_id (int): ID of the user
        limit (int): Maximum number of plans to return
        offset (int): Number of plans to skip

    Returns:
        List[dict]: List of workout plans
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_ALL_WORKOUT_PLANS_BY_USER, (user_id, limit, offset))
        return [
            {
                "workout_plan_id": plan[0],
                "user_id": plan[1],
                "workout_plan_name": plan[2],
                "workout_plan_goal": plan[3],
                "active": plan[4]
            }
            for plan in cursor.fetchall()
        ]


def delete_workout_plan(workout_plan_id: int, user_id: int) -> bool:
    """
    Delete a workout plan.

    Args:
        workout_plan_id (int): ID of the workout plan to delete
        user_id (int): ID of the user owning the plan

    Returns:
        bool: True if workout plan was deleted successfully

    Raises:
        HTTPException: If plan not found
    """
    with cursor_factory() as cursor:
        cursor.execute(DELETE_WORKOUT_PLAN, (workout_plan_id, user_id))
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete workout plan"
            )
        return True


def get_workout_plan_splits(workout_plan_id: int) -> List[dict]:
    """
    Get all splits for a workout plan.

    Args:
        workout_plan_id (int): ID of the workout plan

    Returns:
        List[dict]: List of splits in the workout plan
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_WORKOUT_PLAN_SPLITS, (workout_plan_id,))
        return [
            {
                "split": split[0],
                "workout_plan_id": split[1],
                "active": split[2]
            }
            for split in cursor.fetchall()
        ]


def add_split_to_workout_plan(workout_plan_id: int, split_data: dict) -> bool:
    """
    Add a new split to a workout plan.

    Args:
        workout_plan_id (int): ID of the workout plan
        split_data (dict): Split information

    Returns:
        bool: True if split was added successfully

    Raises:
        HTTPException: If split already exists
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_WORKOUT_SPLIT,
                (
                    split_data["split"],
                    workout_plan_id,
                    split_data.get("active", True)
                )
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Failed to add split to workout plan"
                )
            return True
        except UniqueViolation:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                detail="Split already exists in this workout plan"
            )


def get_split_exercises(
    workout_plan_id: int,
    split: str,
    user_id: int
) -> List[dict]:
    """
    Get all exercises for a specific split.

    Args:
        workout_plan_id (int): ID of the workout plan
        split (str): Name of the split
        user_id (int): ID of the user owning the exercises

    Returns:
        List[dict]: List of exercises in the split
    """
    with cursor_factory() as cursor:
        cursor.execute(
            GET_SPLIT_EXERCISES,
            (workout_plan_id, split, user_id)
        )
        return [
            {
                "workout_plan_id": ex[0],
                "split": ex[1],
                "exercise_id": ex[2],
                "execution_order": ex[3],
                "sets": ex[4],
                "reps": ex[5],
                "advanced_technique": ex[6],
                "rest_time": ex[7],
                "active": ex[8],
                "exercise_name": ex[9],
                "description": ex[10]
            }
            for ex in cursor.fetchall()
        ]


def add_exercise_to_split(workout_plan_id: int, exercise_data: dict) -> bool:
    """
    Add an exercise to a split.

    Args:
        workout_plan_id (int): ID of the workout plan
        exercise_data (dict): Exercise information

    Returns:
        bool: True if exercise was added successfully

    Raises:
        HTTPException: If exercise already exists in split
    """
    with cursor_factory() as cursor:
        try:
            cursor.execute(
                INSERT_SPLIT_EXERCISE,
                (
                    workout_plan_id,
                    exercise_data["split"],
                    exercise_data["exercise_id"],
                    exercise_data["execution_order"],
                    exercise_data["sets"],
                    exercise_data["reps"],
                    exercise_data.get("advanced_technique"),
                    exercise_data["rest_time"],
                    exercise_data.get("active", True)
                )
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Failed to add exercise to split"
                )
            return True
        except UniqueViolation:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                detail="Exercise already exists in this split"
            )