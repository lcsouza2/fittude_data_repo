INSERT_WORKOUT_REPORT = """
    INSERT INTO workout_report (workout_plan_id, report_date, split)
    VALUES (%s, %s, %s)
    RETURNING workout_report_id;
"""

GET_WORKOUT_REPORT_BY_ID = """
    SELECT wr.workout_report_id, wr.workout_plan_id, wr.report_date, wr.split,
           wp.user_id, wp.workout_plan_name
    FROM workout_report wr
    JOIN workout_plan wp ON wp.workout_plan_id = wr.workout_plan_id
    WHERE wr.workout_report_id = %s AND wp.user_id = %s;
"""

GET_WORKOUT_REPORTS_BY_PLAN = """
    SELECT wr.workout_report_id, wr.workout_plan_id, wr.report_date, wr.split
    FROM workout_report wr
    JOIN workout_plan wp ON wp.workout_plan_id = wr.workout_plan_id
    WHERE wr.workout_plan_id = %s AND wp.user_id = %s
    ORDER BY wr.report_date DESC
    LIMIT %s OFFSET %s;
"""

DELETE_WORKOUT_REPORT = """
    DELETE FROM workout_report
    WHERE workout_report_id = %s
    AND workout_plan_id IN (
        SELECT workout_plan_id 
        FROM workout_plan 
        WHERE user_id = %s
    )
    RETURNING workout_report_id;
"""

INSERT_SET_REPORT = """
    INSERT INTO set_report 
    (workout_report_id, exercise_id, split, workout_plan_id, 
     execution_order, set_number, reps, weight, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING workout_report_id;
"""

GET_SET_REPORTS_BY_WORKOUT = """
    SELECT sr.workout_report_id, sr.exercise_id, sr.split, sr.workout_plan_id,
           sr.execution_order, sr.set_number, sr.reps, sr.weight, sr.notes,
           e.exercise_name, e.description
    FROM set_report sr
    JOIN exercise e ON e.exercise_id = sr.exercise_id
    JOIN workout_plan wp ON wp.workout_plan_id = sr.workout_plan_id
    WHERE sr.workout_report_id = %s 
    AND wp.user_id = %s
    ORDER BY sr.execution_order, sr.set_number;
"""

GET_SET_REPORTS_BY_EXERCISE = """
    SELECT sr.workout_report_id, sr.exercise_id, sr.split, sr.workout_plan_id,
           sr.execution_order, sr.set_number, sr.reps, sr.weight, sr.notes,
           wr.report_date
    FROM set_report sr
    JOIN workout_report wr ON wr.workout_report_id = sr.workout_report_id
    JOIN workout_plan wp ON wp.workout_plan_id = sr.workout_plan_id
    WHERE sr.exercise_id = %s 
    AND wp.user_id = %s
    ORDER BY wr.report_date DESC, sr.set_number
    LIMIT %s OFFSET %s;
"""

DELETE_SET_REPORT = """
    DELETE FROM set_report
    WHERE workout_report_id = %s
    AND workout_plan_id IN (
        SELECT workout_plan_id 
        FROM workout_plan 
        WHERE user_id = %s
    )
    RETURNING workout_report_id;
"""