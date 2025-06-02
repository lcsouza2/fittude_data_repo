INSERT_EXERCISE = """
    INSERT INTO exercise (user_id, exercise_name, description, active)
    VALUES (%s, %s, %s, %s)
    RETURNING exercise_id;
"""

UPDATE_EXERCISE = """
    UPDATE exercise
    SET exercise_name = %s, description = %s, active = %s
    WHERE exercise_id = %s AND user_id = %s
    RETURNING exercise_id;
"""

GET_DEFAULT_EXERCISES = """
    SELECT exercise_id, user_id, exercise_name, description, active
    FROM exercise
    WHERE active = true AND user_id IS NULL;
"""

GET_ALL_EXERCISES_BY_USER = """
    SELECT exercise_id, user_id, exercise_name, description, active
    FROM exercise
    WHERE user_id = %s
    LIMIT %s OFFSET %s;
"""

GET_EXERCISE_BY_ID = """
    SELECT exercise_id, user_id, exercise_name, description, active
    FROM exercise
    WHERE exercise_id = %s AND user_id = %s;
"""

GET_EXERCISE_BY_NAME = """
    SELECT exercise_id, user_id, exercise_name, description, active
    FROM exercise
    WHERE exercise_name = %s AND user_id = %s;
"""

DELETE_EXERCISE = """
    DELETE FROM exercise
    WHERE exercise_id = %s AND user_id = %s
    RETURNING exercise_id;
"""

BIND_MUSCLE_TO_EXERCISE = """
    INSERT INTO exercise_muscle (muscle_id, exercise_id)
    VALUES (%s, %s)
    RETURNING exercise_id;
"""

BIND_EQUIPMENT_TO_EXERCISE = """
    INSERT INTO exercise_equipment (equipment_id, exercise_id)
    VALUES (%s, %s)
    RETURNING exercise_id;
"""

GET_EXERCISE_MUSCLES = """
    SELECT m.muscle_id, m.muscle_name, m.group_name
    FROM muscle m
    JOIN exercise_muscle em ON em.muscle_id = m.muscle_id
    WHERE em.exercise_id = %s;
"""

GET_EXERCISE_EQUIPMENT = """
    SELECT e.equipment_id, e.equipment_name, e.group_name
    FROM equipment e
    JOIN exercise_equipment ee ON ee.equipment_id = e.equipment_id
    WHERE ee.exercise_id = %s;
"""
