from sqlalchemy.orm import Session
import app.db.models as models
import app.Models.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from app.Dao.DogDao import adoptar_dog_dao
from datetime import datetime


def get_by_username_dao(db: Session, username: str):
    return db.query(models.User)\
           .filter(models.User.username == username).first()


def create_user_dao(db: Session, user: schemas.UserCreate):
    if get_by_username_dao(db=db, username=user.username) is None:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),
                                        bcrypt.gensalt())
        db_user = models.User(username=user.username,
                                  password=hashed_password,
                                  apellido=user.apellido,
                                  email=user.email)
        try:
            db.add(db_user)
            db.commit()
            return JSONResponse({"message": "Registro exitoso"},
                                status_code=202)
        except Exception:
            return JSONResponse({"message": "Error  base de datos"},
                                status_code=404)
    else:
        return JSONResponse({"message": "Ya existe ese nombre"},
                            status_code=404)
    return db_user


def update_user_dao(db: Session, username_name: str, user: schemas.UserCreate):
    if username_name == user.username:
        return update_aux(db2=db, u=username_name, user2=user)
    else:
        if get_by_username_dao(db=db, username=user.username) is None:
            return update_aux(db2=db, u=username_name, user2=user)

    return JSONResponse({"message": "Ya existe ese nombre"},
                        status_code=404)


def update_aux(db2: Session, u: str, user2: schemas.UserCreate):
    try:
        db2.query(models.User)\
                                .filter(models.User.username == u)\
                                .update({"username": user2.username,
                                         "apellido": user2.apellido,
                                         "email": user2.email})
        db2.commit()

        return JSONResponse({"message": "Actualización exitosa"},
                            status_code=202)
    except Exception:
        return JSONResponse({"message": "Error en la base de datos"},
                            status_code=404)


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    a = get_by_username_dao(db=db, username=user.username)

    return bcrypt.checkpw(user.password.encode('utf-8'),
                          a.password.encode('utf-8'))


def remove_user_dao(db: Session, user_name: str):
    try:
        db.delete(get_by_username_dao(db=db, username=user_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"},
                            status_code=200)
    except Exception:
        return JSONResponse({"message": "Error en la base de datos"},
                            status_code=404)


def get_all_users_dao(db: Session):
    return db.query(models.User).all()


def adoptar_Dao(db: Session, user: models.User, name: str):
    return adoptar_dog_dao(db=db, id=user.id, namedog=name)
