INSERT_USER = """
    INSERT INTO users (email, name, password)
    VALUES (%s, %s, %s)
    RETURNING id;
"""

UPDATE_USER_PASSWORD = """
    UPDATE users
    SET password = %s
    WHERE email = %s;
    RETURNING id;
"""

GET_USER_BY_EMAIL = """
    SELECT id, email, name, password
    FROM users
    WHERE email = %s;
"""

GET_USER_BY_ID = """
    SELECT id, email, name, password
    FROM users
    WHERE id = %s;
"""
