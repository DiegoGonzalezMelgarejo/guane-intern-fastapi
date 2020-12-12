from sqlalchemy.orm import Session
import Models.models as models, db.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from datetime import datetime

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
def remove_dog(db: Session, dog_name: str):
    try:
        db.delete(get_dog(db= db, dog_name=dog_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def get_dog(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()

def get_all_dogs(db: Session):
    return db.query(models.Dog).all()


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


def get_all_dogs2(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted ==1).all()