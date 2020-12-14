# Prueba Técnica


## Tecnologías utilizadas 🚀

-Python
-Docker
-Framework Fastapi(con uvicorn)
-Mysql




### Base de datos📋

_Para conectar o cambiar la base de datos  se debe dirigir al archivo que esta en
app/database y cambiar los datosen estas lineas
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://USER:PASSWORD@"

LINK_AUX = "HOSTNAME/BASEDEDATOS"

Por el momento esta conectado a una rds de aws

```
Da un ejemplo
```

### Despliege 🔧

_docker-compose up --build _

Los endpoints se visualizarian en http://localhost:8000/docs


## Lo realizado ⚙️

_Crud de Perros_<br>
_Crud de Usuarios_
_Listar los adoptados_
_Se implemento autentificación token jwt_
_Permite adoptar perros al usuario en sesion_



⌨️ con ❤️ por [Diego Gonzalez](https://www.linkedin.com/in/diegogonzalez97/) 😊
