from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False)

Session = sessionmaker(bind=engine)
