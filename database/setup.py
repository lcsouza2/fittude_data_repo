from mapping import reg
from sqlalchemy import create_engine
from sqlite3 import connect

engine = create_engine("sqlite:///fittude_repo.db")
reg.metadata.create_all(bind=engine)

