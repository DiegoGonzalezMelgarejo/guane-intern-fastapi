from sqlalchemy.orm import Session
import db.models as models, Models.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from datetime import datetime

def create_new_Dogdao(db: Session, blog: schemas.Dog):

    if get_dogdao(db= db, dog_name=blog.name) is None:
         
        url='https://dog.ceo/api/breeds/image/random'
        response=requests.get(url)
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
        dog = models.Dog(id=blog.id, name=blog.name,picture=response.json()['message'],create_date=timestampStr,is_adopted=blog.is_adopted)
        
        try:
            
            db.add(dog)
            db.commit()
        
            return JSONResponse({"message": "Registro exitoso"}, status_code=202)
        except Exception:
            return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
    else:
        return JSONResponse({"message": "Ya hay un perro con ese nombre"}, status_code=404)
def remove_dogdao(db: Session, dog_name: str):
    try:
        db.delete(get_dogdao(db= db, dog_name=dog_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)

def get_dogdao(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()

def get_all_dogsdao(db: Session):
    return db.query(models.Dog).all()


def update_Dogdao(db: Session, dog_name:str,dog: schemas.Dog):
    if dog_name==dog.name:
        updateaux(db2=db,dog_name2=dog_name,dog2=dog)
    else:
        if get_dogdao(db= db, dog_name=dog.name) is None:
            updateaux(db2=db,dog_name2=dog_name,dog2=dog)
        else:
            return JSONResponse({"message": "Ya hay un perro con ese nombre"}, status_code=404)
        

def updateaux(db2: Session, dog_name2:str,dog2: schemas.Dog):

    try:
        db2.query(models.Dog).filter(models.Dog.name == dog_name).update({"id":blog.id,"name":blog.name})
        db2.commit()
        
        return JSONResponse({"message": "Registro exitoso"}, status_code=202)
    except Exception:
        return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
    


def get_all_dogs2dao(db: Session):
    return db.query(models.Dog,models.UserInfo).join(models.UserInfo).filter(models.Dog.is_adopted ==1).all()

def adoptardogdao(db:Session,id:int,namedog:str):
 
    try:
            db.query(models.Dog).filter(models.Dog.name == namedog).update({"user_id":id,"is_adopted":1})
            db.commit()
        
            return JSONResponse({"message": "Perro adoptado"}, status_code=202)
    except Exception:
            return JSONResponse({"message": "Hubo un error en la base de datos"}, status_code=404)
  
      
