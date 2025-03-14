from fastapi import Depends, HTTPException
from app.firebase.firebaseconfig import get_current_user

async def verify_admin(current_user : dict = Depends(get_current_user)):

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo administradores pueden acceder"
        )
    else:
        return current_user
    
async def verify_user(current_user = Depends(get_current_user)):
    return current_user