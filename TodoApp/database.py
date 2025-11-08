from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# creates an engine through which we can interact with SQL DB
# By setting check_same_thread: False we are allowing multiple threads to interact with the DB
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Set autocommit & autoflush to False to have a full control over the DB
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()