from sqlalchemy.orm import Session
import db.models as models, Models.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from Dao.DogDao import adoptardogdao
from datetime import datetime

def get_user_by_usernamedao(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def create_userdao(db: Session, user: schemas.UserCreate):
    if get_user_by_usernamedao(db= db, username=user.username) is None:
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
def update_Userdao(db: Session, username_name:str,user: schemas.UserCreate):
  
   if username_name==user.username:
       updateaux(db2=db,u=username_name,user2=user)
   else:
       if get_user_by_usernamedao(db= db, username=user.username) is None:
           updateaux(db2=db,u=username_name,user2=user)
       else:
           return JSONResponse({"message": "Ya hay un Usuario con ese nombre"}, status_code=404)

    
def updateaux(db2: Session, u:str,user2: schemas.UserCreate):
    try:
        db2.query(models.UserInfo).filter(models.UserInfo.username == u).update({"username":user2.username,"apellido":user2.apellido,"email":user.email})
        db2.commit()
        
        return JSONResponse({"message": "Actualización exitosa"}, status_code=202)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_usernamedao(db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))







def remove_userdao(db: Session, user_name: str):
    try:
        db.delete(get_user_by_usernamedao(db= db, username=user_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def get_all_usersdao(db: Session):
    return db.query(models.UserInfo).all()
def adoptarDao(db: Session,user:models.UserInfo,name:str):
    return adoptardogdao(db=db,id=user.id,namedog=name)
