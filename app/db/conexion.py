import app.db.models as models
from app.Models.schemas import User, TokenData, UserCreate, Token
from app.db.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
