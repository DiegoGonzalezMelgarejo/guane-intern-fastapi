import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.responses import JSONResponse
import Dao.crud as crud
import db.models as models
import Models.schemas as schemas
from app_utils import decode_access_token
from db.database import engine, SessionLocal
from Models.schemas import UserInfo, TokenData, UserCreate, Token
from db.conexion import get_db
from Dao.UserDao  import get_user_by_usernamedao,check_username_password
from fastapi import APIRouter
post_route = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_usernamedao(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user





@post_route.post("/authenticate", response_model=Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = get_user_by_usernamedao(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            from app_utils import create_access_token
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}