import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from dotenv import load_dotenv, dotenv_values

# Cargar configuración desde .env y variables de entorno
load_dotenv()
config = dotenv_values()
DATABASE_URL = os.getenv("DB_MYSQL_PATH") or config.get("DB_MYSQL_PATH")

class Base(DeclarativeBase):
    pass

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

    def get_session(self) -> Session:
        return self.SessionLocal()

# Instancia única de la base de datos
db_instance = Database()

# Dependencia de FastAPI para obtener la sesión
def get_db():
    db = db_instance.get_session()
    try:
        yield db
    finally:
        db.close()