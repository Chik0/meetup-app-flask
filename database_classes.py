from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer

engine = create_engine('postgresql:///meetup')
session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base(bind=engine)


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False, index=True)