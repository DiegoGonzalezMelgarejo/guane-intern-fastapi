import uvicorn
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
from  db.conexion import get_db
import Rutas.DogRouter as Dogrouter
import Rutas.AuthRouter as Auth
import Rutas.UserRouter as Usuario
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


if __name__ == "__main__":
    
    uvicorn.run(app , host="127.0.0.1", port=8081)