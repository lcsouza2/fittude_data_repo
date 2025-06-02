INSERT_WORKOUT_PLAN = """
    INSERT INTO workout_plan (user_id, workout_plan_name, workout_plan_goal, active)
    VALUES (%s, %s, %s, %s)
    RETURNING workout_plan_id;
"""

UPDATE_WORKOUT_PLAN = """
    UPDATE workout_plan
    SET workout_plan_name = %s, workout_plan_goal = %s, active = %s
    WHERE workout_plan_id = %s AND user_id = %s
    RETURNING workout_plan_id;
"""

GET_WORKOUT_PLAN_BY_ID = """
    SELECT workout_plan_id, user_id, workout_plan_name, workout_plan_goal, active
    FROM workout_plan
    WHERE workout_plan_id = %s AND user_id = %s;
"""

GET_WORKOUT_PLAN_BY_NAME = """
    SELECT workout_plan_id, user_id, workout_plan_name, workout_plan_goal, active
    FROM workout_plan
    WHERE workout_plan_name = %s AND user_id = %s;
"""

GET_ALL_WORKOUT_PLANS_BY_USER = """
    SELECT workout_plan_id, user_id, workout_plan_name, workout_plan_goal, active
    FROM workout_plan
    WHERE user_id = %s AND active = true
    LIMIT %s OFFSET %s;
"""

DELETE_WORKOUT_PLAN = """
    DELETE FROM workout_plan
    WHERE workout_plan_id = %s AND user_id = %s
    RETURNING workout_plan_id;
"""

GET_WORKOUT_PLAN_SPLITS = """
    SELECT split, workout_plan_id, active
    FROM workout_split
    WHERE workout_plan_id = %s;
"""

INSERT_WORKOUT_SPLIT = """
    INSERT INTO workout_split (split, workout_plan_id, active)
    VALUES (%s, %s, %s)
    RETURNING workout_plan_id;
"""

GET_SPLIT_EXERCISES = """
    SELECT se.workout_plan_id, se.split, se.exercise_id, se.execution_order,
           se.sets, se.reps, se.advanced_technique, se.rest_time, se.active,
           e.exercise_name, e.description
    FROM split_exercise se
    JOIN exercise e ON e.exercise_id = se.exercise_id
    WHERE se.workout_plan_id = %s 
          AND se.split = %s 
          AND e.user_id = %s
          AND se.active = true
    ORDER BY se.execution_order;
"""

INSERT_SPLIT_EXERCISE = """
    INSERT INTO split_exercise 
    (workout_plan_id, split, exercise_id, execution_order, sets, reps, 
     advanced_technique, rest_time, active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING workout_plan_id;
"""
