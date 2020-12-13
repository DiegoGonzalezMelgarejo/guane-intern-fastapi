from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://admin:12345678@guane-intern-fastapi.cs1utmreikc4.us-east-1.rds.amazonaws.com:3306/guane-intern-fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()