from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import config


app_session = None

engine = create_engine(config.DATABASE_URL, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
