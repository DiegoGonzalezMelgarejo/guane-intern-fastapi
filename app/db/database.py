from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:12345678@"

LINK_AUX = "prueba.cs1utmreikc4.us-east-1.rds.amazonaws.com/prueba"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL + LINK_AUX,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
