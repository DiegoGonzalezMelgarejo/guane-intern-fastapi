from sqlalchemy.orm import Session
import db.models as models, Models.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from Dao.DogDao import adoptardog
from datetime import datetime

def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_username(db= db, username=user.username) is None:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db_user = models.UserInfo(username=user.username, password=hashed_password, apellido=user.apellido,email=user.email)
        
        try:
                     
            db.add(db_user)
            db.commit()
        
            return JSONResponse({"message": "Registro exitoso"}, status_code=202)
        except Exception:
            return JSONResponse({"message": Exception.__name__}, status_code=404)
    else:
        return JSONResponse({"message": "Ya hay un Usuario con ese nombre"}, status_code=404)
    return db_user
def update_User(db: Session, username_name:str,user: schemas.UserCreate):
  
    
    try:


        db.query(models.UserInfo).filter(models.UserInfo.username == username_name).update({"username":user.username,"apellido":user.apellido,"email":user.email})
        db.commit()
        
        return JSONResponse({"message": "Registro exitoso"}, status_code=202)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
    

def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_username(db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))







def remove_user(db: Session, user_name: str):
    try:
        db.delete(get_user_by_username(db= db, username=user_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def get_all_users(db: Session):
    return db.query(models.UserInfo).all()
def adoptarDao(db: Session,user:models.UserInfo,name:str):
    return adoptardog(db=db,id=user.id,namedog=name)
