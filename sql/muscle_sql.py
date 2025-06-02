INSERT_MUSCLE = """
    INSERT INTO muscle (user_id, group_name, muscle_name, active)
    VALUES (%s, %s, %s, %s)
    RETURNING muscle_id;
"""

UPDATE_MUSCLE = """
    UPDATE muscle
    SET group_name = %s, muscle_name = %s, active = %s
    WHERE muscle_id = %s AND user_id = %s;
    RETURNING muscle_id;
"""

GET_DEFAULT_MUSCLES = """
    SELECT muscle_id, user_id, group_name, muscle_name, active
    FROM muscle
    WHERE active = true AND user_id IS NULL;
"""

GET_ALL_MUSCLES_BY_USER = """
    SELECT muscle_id, user_id, group_name, muscle_name, active
    FROM muscle
    WHERE user_id = %s
    LIMIT %s OFFSET %s
"""

GET_MUSCLE_BY_ID = """
    SELECT muscle_id, user_id, group_name, muscle_name, active
    FROM muscle
    WHERE muscle_id = %s AND user_id = %s;
"""

GET_MUSCLE_BY_NAME = """
    SELECT muscle_id, user_id, group_name, muscle_name, active
    FROM muscle
    WHERE muscle_name = %s AND user_id = %s;
"""

DELETE_MUSCLE = """
    DELETE FROM muscle
    WHERE muscle_id = %s AND user_id = %s;
    RETURNING muscle_id;
"""
