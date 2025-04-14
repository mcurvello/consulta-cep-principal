import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from model.base import Base
from model.consulta import Consulta

db_path = "database/"

if not os.path.exists(db_path):
    os.makedirs(db_path)

# Define a URL do banco SQLite
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria o engine do SQLAlchemy
engine = create_engine(db_url, echo=False)

# Verifica se o banco já existe, senão cria
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas definidas nos modelos
Base.metadata.create_all(engine)

# Cria a sessão
Session = sessionmaker(bind=engine)
