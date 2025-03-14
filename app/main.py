from fastapi import FastAPI, Header, HTTPException, Depends
from app.controller import package_controller
from app.database.database import Base, db_instance
from app.controller import user_controller
from app.controller import transaction_controller
from app.firebase.firebaseconfig import get_current_user
from app.auth.auth import verify_admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=db_instance.engine)

API_DESCRIPTION = """
API para la gestión del club de pádel. 

## Funcionalidades

* 👤 Gestión de usuarios
* 🎫 Sistema de tickets
* 📦 Paquetes de tickets
* 💳 Transacciones
* 🔐 Autenticación con Firebase
"""

app = FastAPI(
    title="Padel de Ituzaingo",
    description=API_DESCRIPTION,
    version="1.0.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,           # Usamos el título ya definido
        version=app.version,       # Usamos la versión ya definida
        description=app.description, # Usamos la descripción ya definida
        routes=app.routes,
    )
    
    #Autenticación
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solo este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(user_controller.router, tags=["Users"], prefix="/user")
app.include_router(package_controller.router, tags=["Packages"], prefix="/package")
app.include_router(transaction_controller.router, tags=["Transactions"], prefix="/transaction")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/login/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {
        "message": "Protected route",
        "firebase_uid": current_user.get("uid"),
        "email": current_user.get("email")
    }

# Test para verificar admin
@app.get("/admin")
async def verify_admin(current_user = Depends(verify_admin)):
    return {
        current_user
    }

#averiguar para alojamiento, AWS, Azure, Google Cloud, etc. 
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


from fastapi import FastAPI

from app.dynatrace_client import enviar_metrica


app = FastAPI()

@app.get("/ping")
async def ping():
    for i in range(3):
        enviar_metrica("app.requests", 1, "count")
    print("salio del for")
    return {"message": "pong"}

@app.get("/usuarios")
async def obtener_usuarios():
    enviar_metrica("usuarios.consultados", 1, "count")
    return {"usuarios": ["Sebastián", "Carlos", "María"]}
