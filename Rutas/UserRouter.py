import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.responses import JSONResponse

import db.models as models
import Models.schemas as schemas
from app_utils import decode_access_token
from db.database import engine, SessionLocal
from Models.schemas import UserInfo, TokenData, UserCreate, Token
from db.conexion import get_db
from Dao.UserDao  import get_all_users,get_user_by_username,update_User,create_user,remove_user,adoptarDao
from fastapi import APIRouter
from Rutas.AuthRouter import get_current_user, get_user_by_username
post_route = APIRouter()


@post_route.get("/user")
async def get_all_userss(db: Session = Depends(get_db)):
    return get_all_users(db=db)
@post_route.get("/user/{user_name}")
async def get_users_by_username(user_name,db: Session = Depends(get_db)):
    return get_user_by_username(db= db, username=user_name)
@post_route.put("/user/{user_name}", response_model=schemas.Dog)
async def update_User(user: schemas.UserCreate, user_name,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return update_User(db=db, username_name=user_name, user=user)
@post_route.post("/user", response_model=UserInfo)
def create_users(user: UserCreate, db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return create_user(db=db, user=user)

@post_route.delete("/user/{user_name}")
def deleteuser(user_name, db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return remove_user(db=db, user_name=user_name)

@post_route.put("/user/adoptar/{namedog}")
async def adopt( namedog,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return adoptarDao(db=db,user=current_user,name=namedog)