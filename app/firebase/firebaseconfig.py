from fastapi import HTTPException, Header, status, Security
import firebase_admin 
from firebase_admin import credentials, auth, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from firebase_admin import firestore

class FirebaseAuth:
    def __init__(self, credentials_path: str):

        try:
            #Inicializar Firebase Admin SDK solo si no se ha inicializado previamente
            if not firebase_admin._apps:
                self.cred = credentials.Certificate(credentials_path)
                self.app = initialize_app(self.cred)
        except Exception as e:
            raise RuntimeError(f"Error initializing Firebase: {e}")
    
    async def verify_token(self, token: str) -> Dict:
        if type(token) != str:
            return HTTPException(status_code=401, detail="El token no es un string")
        try:
            return auth.verify_id_token(token)
        except auth.ExpiredIdTokenError:
            raise HTTPException(
                status_code=401, 
                detail="Expired token. Login again."
                )
        except auth.RevokedIdTokenError:
            raise HTTPException(
                status_code=401, 
                detail="Revoked token."
                )
        except auth.InvalidIdTokenError:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token."
                )
        except Exception as e:
            raise HTTPException(
                status_code=401, 
                detail=f"Authentication failed: {str(e)}"
                )

# Variables globales que contienen la unica instancia de FirebaseAuth y Db de firestore
_firebase_auth_instance = None
db_firestore = None

async def get_firebase_auth() -> FirebaseAuth:
    global _firebase_auth_instance
    if (_firebase_auth_instance == None):
        _firebase_auth_instance = FirebaseAuth("app/firebase_config.json")
    return _firebase_auth_instance

async def get_firestore_db():
    global db_firestore
    if (db_firestore == None):
        db_firestore = firestore.client()
    return db_firestore

async def get_current_user(authorization: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> Dict:
    firebase_auth = await get_firebase_auth()
    firestore_db = await get_firestore_db()

    decoded_token = await firebase_auth.verify_token(authorization.credentials)

    user_ref = firestore_db.collection("users").document(decoded_token["uid"])
    user_doc = user_ref.get()

    if user_doc.exists:
        decoded_token["role"] = user_doc.to_dict().get("role", "user")

    return decoded_token