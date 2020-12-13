from sqlalchemy.orm import Session
import app.db.models as models
import app.Models.schemas as schemas
import bcrypt
from fastapi.responses import JSONResponse
import requests
from datetime import datetime


def create_new_dog_dao(db: Session, blog: schemas.Dog):
    if get_dog_dao(db=db, dog_name=blog.name) is None:

        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url)
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
        dog = models.Dog(id=blog.id, name=blog.name,
                         picture=response.json()['message'],
                         create_date=timestampStr,
                         is_adopted=blog.is_adopted)

        try:

            db.add(dog)
            db.commit()
            return JSONResponse({"message": "Registro exitoso"},
                                status_code=202)

        except Exception:

            return JSONResponse({"message": "Error base de datos"},
                                status_code=404)

    else:
        return JSONResponse({"message": "Ya hay un perro con ese nombre"},
                            status_code=404)


def remove_dog_dao(db: Session, dog_name: str):

    try:
        db.delete(get_dog_dao(db=db, dog_name=dog_name))
        db.commit()
        return JSONResponse({"message": "Elimino Correctamente"},
                            status_code=200)
    except Exception:
        return JSONResponse({"message": "Hubo base de datos"},
                            status_code=404)


def get_dog_dao(db: Session, dog_name: str):

    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()


def get_all_dogs_dao(db: Session):

    return db.query(models.Dog).all()


def update_dog_dao(db_dao: Session, dog_name_dao: str, dog_dao: schemas.Dog):

    if dog_name_dao == dog_dao.name:
        update_aux(db2=db_dao, dog_name2=dog_name_dao, dog2=dog_dao)
    else:
        if get_dog_dao(db=db_dao, dog_name=dog_dao.name) is None:
            update_aux(db2=db_dao, dog_name2=dog_name_dao, dog2=dog_dao)
        else:
            return JSONResponse({"message": "Ya existe ese nombre"},
                                status_code=404)


def update_aux(db2: Session, dog_name2: str, dog2: schemas.Dog):

    try:

        db2.query(models.Dog).filter(models.Dog.name == dog_name2)\
            .update({"id": dog2.id, "name": dog2.name})
        db2.commit()
        return JSONResponse({"message": "Registro exitoso"},
                            status_code=202)
    except Exception:

        return JSONResponse({"message": "Error base de datos"},
                            status_code=404)


def get_all_dogs_adopted_dao(db: Session):

    return db.query(models.Dog, models.User)\
             .join(models.User).filter(models.Dog.is_adopted == 1).all()


def adoptar_dog_dao(db: Session, id: int, namedog: str):
    try:
        db.query(models.Dog)\
          .filter(models.Dog.name == namedog)\
          .update({"user_id": id, "is_adopted": 1})

        db.commit()
        return JSONResponse({"message": "Perro adoptado"},
                            status_code=202)
    except Exception:
        return JSONResponse({"message": "Error base de datos"},
                            status_code=404)
