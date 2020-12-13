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
from app.Dao.UserDao import get_by_username_dao
from app.db.database import engine, SessionLocal
from app.Models.schemas import User, TokenData, UserCreate, Token
from app.db.conexion import get_db
from app.Dao.DogDao import create_new_dog_dao, get_dog_dao, remove_dog_dao
from app.Dao.DogDao import update_dog_dao, get_all_dogs_adopted_dao
from app.Dao.DogDao import get_all_dogs_dao
from app.Rutas.AuthRouter import get_current_user

from fastapi import APIRouter
post_route = APIRouter()


@post_route.delete("/dog/{dog_name}")
async def remove(dog_name, db: Session=Depends(get_db),
                 current_user: User=Depends(get_current_user)):

    return remove_dog_dao(db=db, dog_name=dog_name)


@post_route.post("/dog", response_model=schemas.Dog)
async def create_new_dog(blog: schemas.Dog, db: Session=Depends(get_db),
                         current_user: User=Depends(get_current_user)):
    return create_new_dog_dao(db=db, blog=blog)


@post_route.get("/dog")
async def get_all_dog(db: Session=Depends(get_db)):
    return get_all_dogs_dao(db=db)


@post_route.get("/dog/is_adopted")
async def get_all_dogs_adopted(db: Session=Depends(get_db)):
    return get_all_dogs_adopted_dao(db=db)


@post_route.get("/dog/{dog_name}")
async def get_dog_by_name(dog_name, db: Session=Depends(get_db)):
    return get_dog_dao(db=db, dog_name=dog_name)


@post_route.put("/dog/{dog_name}", response_model=schemas.Dog)
async def update_dog(dog: schemas.Dog, dog_name, db: Session=Depends(get_db),
                     current_user: User=Depends(get_current_user)):
    return update_dog_dao(db_dao=db, dog_name_dao=dog_name, dog_dao=dog)
