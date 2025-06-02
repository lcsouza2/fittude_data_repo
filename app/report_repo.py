from fastapi import HTTPException
from http import HTTPStatus
from typing import List
from utils import cursor_factory
from sql.report_sql import *


def create_workout_report(workout_plan_id: int, report_data: dict) -> bool:
    """
    Create a new workout report.

    Args:
        workout_plan_id (int): ID of the workout plan
        report_data (dict): Report data containing date and split

    Returns:
        bool: True if report was created successfully

    Raises:
        HTTPException: If creation fails
    """
    with cursor_factory() as cursor:
        cursor.execute(
            INSERT_WORKOUT_REPORT,
            (
                workout_plan_id,
                report_data["report_date"],
                report_data["split"]
            )
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create workout report"
            )
        return True


def get_workout_report_by_id(workout_report_id: int, user_id: int) -> dict:
    """
    Get a workout report by its ID.

    Args:
        workout_report_id (int): ID of the workout report to retrieve
        user_id (int): ID of the user owning the report

    Returns:
        dict: Workout report information

    Raises:
        HTTPException: If report not found
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_WORKOUT_REPORT_BY_ID, (workout_report_id, user_id))
        report = cursor.fetchone()
        if not report:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail="Workout report not found"
            )
        return {
            "workout_report_id": report[0],
            "workout_plan_id": report[1],
            "report_date": report[2],
            "split": report[3],
            "user_id": report[4],
            "workout_plan_name": report[5]
        }


def get_workout_reports_by_plan(
    workout_plan_id: int,
    user_id: int,
    limit: int = 10,
    offset: int = 0
) -> List[dict]:
    """
    Get all workout reports for a plan with pagination.

    Args:
        workout_plan_id (int): ID of the workout plan
        user_id (int): ID of the user owning the plan
        limit (int): Maximum number of reports to return
        offset (int): Number of reports to skip

    Returns:
        List[dict]: List of workout reports
    """
    with cursor_factory() as cursor:
        cursor.execute(
            GET_WORKOUT_REPORTS_BY_PLAN,
            (workout_plan_id, user_id, limit, offset)
        )
        return [
            {
                "workout_report_id": report[0],
                "workout_plan_id": report[1],
                "report_date": report[2],
                "split": report[3]
            }
            for report in cursor.fetchall()
        ]


def delete_workout_report(workout_report_id: int, user_id: int) -> bool:
    """
    Delete a workout report.

    Args:
        workout_report_id (int): ID of the workout report to delete
        user_id (int): ID of the user owning the report

    Returns:
        bool: True if report was deleted successfully

    Raises:
        HTTPException: If report not found or deletion fails
    """
    with cursor_factory() as cursor:
        cursor.execute(DELETE_WORKOUT_REPORT, (workout_report_id, user_id))
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete workout report"
            )
        return True


def create_set_report(workout_report_id: int, set_data: dict) -> bool:
    """
    Create a new set report.

    Args:
        workout_report_id (int): ID of the workout report
        set_data (dict): Set information

    Returns:
        bool: True if set report was created successfully

    Raises:
        HTTPException: If creation fails
    """
    with cursor_factory() as cursor:
        cursor.execute(
            INSERT_SET_REPORT,
            (
                workout_report_id,
                set_data["exercise_id"],
                set_data["split"],
                set_data["workout_plan_id"],
                set_data["execution_order"],
                set_data["set_number"],
                set_data["reps"],
                set_data["weight"],
                set_data.get("notes")
            )
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create set report"
            )
        return True


def get_set_reports_by_workout(workout_report_id: int, user_id: int) -> List[dict]:
    """
    Get all set reports for a workout.

    Args:
        workout_report_id (int): ID of the workout report
        user_id (int): ID of the user owning the report

    Returns:
        List[dict]: List of set reports
    """
    with cursor_factory() as cursor:
        cursor.execute(GET_SET_REPORTS_BY_WORKOUT, (workout_report_id, user_id))
        return [
            {
                "workout_report_id": report[0],
                "exercise_id": report[1],
                "split": report[2],
                "workout_plan_id": report[3],
                "execution_order": report[4],
                "set_number": report[5],
                "reps": report[6],
                "weight": report[7],
                "notes": report[8],
                "exercise_name": report[9],
                "description": report[10]
            }
            for report in cursor.fetchall()
        ]


def get_set_reports_by_exercise(
    exercise_id: int,
    user_id: int,
    limit: int = 10,
    offset: int = 0
) -> List[dict]:
    """
    Get exercise history with pagination.

    Args:
        exercise_id (int): ID of the exercise
        user_id (int): ID of the user owning the exercise
        limit (int): Maximum number of reports to return
        offset (int): Number of reports to skip

    Returns:
        List[dict]: List of set reports for the exercise
    """
    with cursor_factory() as cursor:
        cursor.execute(
            GET_SET_REPORTS_BY_EXERCISE,
            (exercise_id, user_id, limit, offset)
        )
        return [
            {
                "workout_report_id": report[0],
                "exercise_id": report[1],
                "split": report[2],
                "workout_plan_id": report[3],
                "execution_order": report[4],
                "set_number": report[5],
                "reps": report[6],
                "weight": report[7],
                "notes": report[8],
                "report_date": report[9]
            }
            for report in cursor.fetchall()
        ]


def delete_set_report(workout_report_id: int, user_id: int) -> bool:
    """
    Delete set reports for a workout.

    Args:
        workout_report_id (int): ID of the workout report
        user_id (int): ID of the user owning the report

    Returns:
        bool: True if set reports were deleted successfully

    Raises:
        HTTPException: If deletion fails
    """
    with cursor_factory() as cursor:
        cursor.execute(DELETE_SET_REPORT, (workout_report_id, user_id))
        if cursor.fetchone() is None:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete set report"
            )
        return True