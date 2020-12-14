# Prueba Técnica


## Tecnologías utilizadas 🚀

-Python<br>
-Docker<br>
-Framework Fastapi(con uvicorn)<br>
-Mysql<br>




### Base de datos📋

_Para conectar o cambiar la base de datos  se debe dirigir al archivo que esta en
app/database y cambiar los datos en estas lineas<br>
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://USER:PASSWORD@"

LINK_AUX = "HOSTNAME/BASEDEDATOS"<br>
Actualmente se esta conectando a una base de datos de una rds en aws<br>

### Despliege 🔧
<br>
docker-compose up --build 

Los endpoints se visualizarian en http://localhost:8000/docs


## Lo realizado ⚙️

_Crud de Perros_<br>
_Crud de Usuarios_<br>
_Listar los adoptados_<br>
_Se implemento autentificación token jwt_<br>
_Permite adoptar perros al usuario en sesion_<br>

⌨️ con ❤️ por [Diego Gonzalez](https://www.linkedin.com/in/diegogonzalez97/) 😊
