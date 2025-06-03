from mapping import reg
from sqlalchemy import create_engine, text
import sqlite3

engine = create_engine("sqlite:///.fittude_repo.db")
reg.metadata.create_all(bind=engine)

with open("./database/default_data.sql", "r") as sql_file:
    with sqlite3.connect(".fittude_repo.db") as conn:
        conn.executescript(sql_file.read())