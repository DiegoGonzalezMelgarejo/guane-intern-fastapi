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
from app.Dao.UserDao import get_user_by_usernamedao
from app.db.database import engine, SessionLocal
from app.Models.schemas import UserInfo, TokenData, UserCreate, Token
from app.db.conexion import get_db
from app.Dao.DogDao import create_new_Dogdao,get_dogdao,remove_dogdao,get_all_dogsdao,get_all_dogs2dao,update_Dogdao
from app.Rutas.AuthRouter import get_current_user

from fastapi import APIRouter
post_route = APIRouter()
@post_route.delete("/dog/{dog_name}")
async def remove(dog_name,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return remove_dogdao(db=db, dog_name=dog_name)

@post_route.post("/dog", response_model=schemas.Dog)
async def create_new_dog(blog: schemas.Dog,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return create_new_Dogdao(db=db, blog=blog)

@post_route.get("/dog")
async def get_all_dog(db: Session = Depends(get_db)):
    return get_all_dogsdao(db=db)

@post_route.get("/dog/is_adopted")
async def dog_adoptado(db: Session = Depends(get_db)):
    return get_all_dogs2dao(db=db)
@post_route.get("/dog/{dog_name}")
async def get_dog_by_name(dog_name,db: Session = Depends(get_db)):
    return get_dogdao(db=db, dog_name=dog_name)
@post_route.put("/dog/{dog_name}", response_model=schemas.Dog)
async def update_dog(blog: schemas.Dog, dog_name,db: Session = Depends(get_db),current_user: UserInfo = Depends(get_current_user)):
    return update_Dogdao(db=db, dog_name=dog_name, dog=blog)
