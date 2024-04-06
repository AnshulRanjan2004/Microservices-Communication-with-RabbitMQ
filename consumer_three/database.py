from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'sqlite:///database.db'

engine = create_engine(URL_DATABASE)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()