import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.responses import JSONResponse

import app.db.models as models
import app.Models.schemas as schemas
from app.app_utils import decode_access_token
from app.db.database import engine, SessionLocal
from app.Models.schemas import User, TokenData, UserCreate, Token
from app.db.conexion import get_db
from app.Dao.UserDao import get_by_username_dao, check_username_password
from fastapi import APIRouter
post_route = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")
EXPIRE_MINUTES = 30
async def get_current_user(token=Depends(oauth2_scheme),
                           db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(data=token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_by_username_dao(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@post_route.post("/authenticate", response_model=Token)
def authenticate_user(user: schemas.UserAuthenticate,
                      db: Session=Depends(get_db)):
    db_user = get_by_username_dao(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400,
                                detail="Password is not correct")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=EXPIRE_MINUTES)
            from app.app_utils import create_access_token
            a = create_access_token(data={"sub": user.username},
                                    expires_delta=access_token_expires)
            return {"access_token": a,
                    "token_type": "Bearer"}
