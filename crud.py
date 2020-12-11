from sqlalchemy.orm import Session
import models, schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from datetime import datetime
def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(username=user.username, password=hashed_password, apellido=user.apellido,email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_username(db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))


def create_new_blog(db: Session, blog: schemas.BlogBase):
    db_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_all_blogs(db: Session):
    return db.query(models.Blog).all()


def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def create_new_Dog(db: Session, blog: schemas.Dog):

    if get_dog(db= db, dog_name=blog.name) is None:
         
        url='https://dog.ceo/api/breeds/image/random'
        response=requests.get(url)
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
        db_blog = models.Dog(id=blog.id, name=blog.name,picture=response.json()['message'],create_date=timestampStr,is_adopted=blog.is_adopted)
        
        try:
            
            db.add(db_blog)
            db.commit()
        
            return JSONResponse({"message": "Registro exitoso"}, status_code=202)
        except Exception:
            return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
    else:
        return JSONResponse({"message": "Ya hay un perro con ese nombre"}, status_code=404)


def update_Dog(db: Session, dog_name:str,blog: schemas.Dog):
    if get_dog(db= db, dog_name=blog.name) is None:
        try:
            db.query(models.Dog).filter(models.Dog.name == dog_name).update({"id":blog.id,"name":blog.name})
            db.commit()
        
            return JSONResponse({"message": "Registro exitoso"}, status_code=202)
        except Exception:
            return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
    else:
        return JSONResponse({"message": "Ya hay un perro con ese nombre"}, status_code=404)


def get_all_dogs(db: Session):
    return db.query(models.Dog).all()
def get_all_users(db: Session):
    return db.query(models.UserInfo).all()
def get_all_dogs2(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted ==1).all()

def remove_dog(db: Session, dog_name: str):
    try:
        db.delete(get_dog(db= db, dog_name=dog_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def get_dog(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()

def get_all_dogs_adop(db: Session):

    return db.query(models.Dog).all()

    
