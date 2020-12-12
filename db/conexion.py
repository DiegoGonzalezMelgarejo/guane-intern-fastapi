import db.models as models
from Models.schemas import UserInfo, TokenData, UserCreate, Token
from db.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()