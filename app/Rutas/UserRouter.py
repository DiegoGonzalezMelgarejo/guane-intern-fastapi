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
from app.Models.schemas import UserInfo, TokenData, UserCreate, Token
from app.db.conexion import get_db
from app.Dao.UserDao  import get_all_usersdao,get_user_by_usernamedao,update_Userdao,create_userdao,remove_userdao,adoptarDao
from fastapi import APIRouter
from app.Rutas.AuthRouter import get_current_user
post_route = APIRouter()


@post_route.get("/user")
async def get_all_userss(db: Session = Depends(get_db)):
    return get_all_usersdao(db=db)
@post_route.get("/user/{user_name}")
async def get_users_by_username(user_name,db: Session = Depends(get_db)):
    return get_user_by_usernamedao(db= db, username=user_name)
@post_route.put("/user/{user_name}", response_model=schemas.Dog)
async def update_User(user: schemas.UserCreate, user_name,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return update_Userdao(db=db, username_name=user_name, user=user)
@post_route.post("/user", response_model=UserInfo)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    return create_userdao(db=db, user=user)

@post_route.delete("/user/{user_name}")
def deleteuser(user_name, db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return remove_userdao(db=db, user_name=user_name)

@post_route.put("/user/adoptar/{namedog}")
async def adopt( namedog,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return adoptarDao(db=db,user=current_user,name=namedog)