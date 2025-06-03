from mapping import reg
from sqlalchemy import create_engine

engine = create_engine("sqlite:///fittude_repo.db")
reg.metadata.create_all(bind=engine)

