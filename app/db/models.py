from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from app.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))
    apellido = Column(String(100))
    email = Column(String(100))


class Dog(Base):
    __tablename__ ="dog"

    id=Column(String(100),primary_key=True)
    name = Column(String(100))
    picture = Column(String(500))
    create_date = Column(String(100))
    is_adopted = Column(Boolean)
    user_id = Column( ForeignKey("user.id"))
    
    










