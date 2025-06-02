INSERT_EQUIPMENT = """
    INSERT INTO equipment (user_id, group_name, equipment_name, active)
    VALUES (%s, %s, %s, %s)
    RETURNING equipment_id;
"""

UPDATE_EQUIPMENT = """
    UPDATE equipment
    SET group_name = %s, equipment_name = %s, active = %s
    WHERE equipment_id = %s AND user_id = %s;
    RETURNING equipment_id;
"""

GET_DEFAULT_EQUIPMENT = """
    SELECT equipment_id, user_id, group_name, equipment_name, active
    FROM equipment
    WHERE active = true AND user_id = null;
"""

GET_ALL_EQUIPMENT_BY_USER = """
    SELECT equipment_id, user_id, group_name, equipment_name, active
    FROM equipment
    WHERE user_id = %s
    LIMIT %s OFFSET %s;
"""

GET_EQUIPMENT_BY_ID = """
    SELECT equipment_id, user_id, group_name, equipment_name, active
    FROM equipment
    WHERE equipment_id = %s AND user_id = %s;
"""

GET_EQUIPMENT_BY_NAME = """
    SELECT equipment_id, user_id, group_name, equipment_name, active
    FROM equipment
    WHERE equipment_name = %s AND user_id = %s;
"""

DELETE_EQUIPMENT = """
    DELETE FROM equipment
    WHERE equipment_id = %s AND user_id = %s;
    RETURNING equipment_id;
"""
