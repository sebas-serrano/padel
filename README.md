# Padel de Ituzaingo API - How to

API para la gestión del club de pádel desarrollada con FastAPI.

## 📋 Requisitos Previos

- [Python 3.8+](https://www.python.org/downloads)
- [MySQL](https://www.mysql.com/downloads/)
- [Cuenta de Firebase y configuarción](https://firebase.google.com/?hl=es-419)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

## 🔧 Instalación

**1.Clonar el repositorio:**

- git clone a la [URL de este repositorio](https://github.com/ignaciordgz/RetoPadelBackend)

**2.Crear Entorno Virtual:**

- En la terminal de VSCode ejecutar el comando:

- python -m venv venv

- Después ejecutar:

***En Linux/Mac***: source venv/bin/activate  

***En Windows:*** env\Scripts\activate

**3.Instalar Dependecias:**

- pip install -r requirements.txt
- $env:PYTHONPATH = (Get-Location).Path pytest tests/ **en caso de falla usar: `python -m pytest tests/`**

**4.Configurar variables de entorno y crear Base de Datos en Workbench.**

- Crear archivo en la carpeta RetoPadelBackend llamado "`.env`" con el contenido:
    - "`DB_MYSQL_PATH = "mysql+pymysql://-{nombre:contraseña}@localhost:3306/{nombrebd}"`", deberia de quedar algo asi: DB_MYSQL_PATH = "mysql+pymysql://root:aspire@localhost:3306/padel"
    - En caso de necesitar probar los tests, deben agregar el campo: "`ADMIN_TOKEN="Bearer <Token>`" en el mismo "`.env`" donde agregaron el "`DB_MYSQL_PATH`"
- En Workbench crear la base de datos - `CREATE DATABASE + nombre` -
- En Workbench usar la base de datos creada - `USE DATABASE + nombre` -

**5.Rol de admistrador en Firebase:**

- Contactar a Soporte

**6.Ejecutar el proyecto:**

- uvicorn main:app --reload
  
**7.Ejecutar un test:**

- pytest tests/test_<nombre_test>.py
- pytest tests/test_<nombre_test>.py::<nombre_de_funcion> 

**8.Probar la API:**

- Dirigirse a la URL del proyecto ejecutado que nos da la terminal para interactuar con el Swagger y probar la API.
