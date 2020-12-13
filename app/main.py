import uvicorn
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
from  app.db.conexion import get_db
import app.Rutas.DogRouter as Dogrouter
import app.Rutas.AuthRouter as Auth
import app.Rutas.UserRouter as Usuario
models.Base.metadata.create_all(bind=engine)



app = FastAPI()
origins = [
    "http://localhost:4200",
    "localhost:4200"
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)
# Dependency



app.include_router(Auth.post_route, prefix="/api")
app.include_router(Dogrouter.post_route, prefix="/api")
app.include_router(Usuario.post_route, prefix="/api")


