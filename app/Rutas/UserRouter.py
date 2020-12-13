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
from app.Dao.UserDao import get_all_users_dao, get_by_username_dao
from app.Dao.UserDao import update_user_dao, create_user_dao, remove_user_dao
from app.Dao.UserDao import remove_user_dao, adoptar_Dao
from fastapi import APIRouter
from app.Rutas.AuthRouter import get_current_user
post_route = APIRouter()


@post_route.get("/user")
async def get_all_users(db: Session=Depends(get_db)):
    return get_all_users_dao(db=db)


@post_route.get("/user/{user_name}")
async def get_users_by_username(user_name, db: Session=Depends(get_db)):
    return get_by_username_dao(db=db, username=user_name)


@post_route.put("/user/{user_name}", response_model=schemas.Dog)
async def update_User(user: schemas.UserCreate, user_name,
                      db: Session=Depends(get_db),
                      current_user: User=Depends(get_current_user)):
    return update_user_dao(db=db, username_name=user_name, user=user)


@post_route.post("/user", response_model=User)
def create_users(user: UserCreate, db: Session=Depends(get_db)):
    return create_user_dao(db=db, user=user)


@post_route.delete("/user/{user_name}")
def deleteuser(user_name, db: Session=Depends(get_db),
               current_user: User=Depends(get_current_user)):
    return remove_user_dao(db=db, user_name=user_name)


@post_route.put("/user/adoptar/{namedog}")
async def adopt(namedog, db: Session=Depends(get_db),
                current_user: User=Depends(get_current_user)):
    return adoptar_Dao(db=db, user=current_user, name=namedog)
