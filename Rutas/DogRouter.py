import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.responses import JSONResponse

import Models.models as models
import db.schemas as schemas
from app_utils import decode_access_token
from Dao.UserDao import get_user_by_username
from db.database import engine, SessionLocal
from db.schemas import UserInfo, TokenData, UserCreate, Token
from db.conexion import get_db
from Dao.DogDao import create_new_Dog,get_dog,remove_dog,get_all_dogs,get_all_dogs2,update_Dog
from fastapi import APIRouter
post_route = APIRouter()
@post_route.delete("/dog/{dog_name}")
async def remove(dog_name,db: Session = Depends(get_db)):
    return remove_dog(db=db, dog_name=dog_name)

@post_route.post("/dog", response_model=schemas.Dog)
async def create_new_dog(blog: schemas.Dog, 
                         db: Session = Depends(get_db)):
    return create_new_Dog(db=db, blog=blog)

@post_route.get("/dog")
async def get_all_dog(db: Session = Depends(get_db)):
    return get_all_dogs(db=db)

@post_route.get("/dog/is_adopted")
async def dog_adoptado(db: Session = Depends(get_db)):
    return get_all_dogs2(db=db)
@post_route.get("/dog/{dog_name}")
async def get_dog_by_name(dog_name,db: Session = Depends(get_db)):
    return get_dog(db=db, dog_name=dog_name)
@post_route.put("/dog/{dog_name}", response_model=schemas.Dog)
async def update_dog(blog: schemas.Dog, dog_name,db: Session = Depends(get_db)):
    return update_Dog(db=db, dog_name=dog_name, blog=blog)
