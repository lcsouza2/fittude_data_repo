from psycopg2 import connect


def cursor_factory():
    """
    Factory function to create a database connection.

    Returns:
        psycopg2.cursor: A cursor to the PostgreSQL database.
    """
    return connect(
        user="your_user",
        password="your_password",
        database="your_database",
        host="localhost",
        port=5432,
    ).cursor()
