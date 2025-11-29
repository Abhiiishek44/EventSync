from datetime import datetime, timedelta
from jose import jwt, JWTError
import os 
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database.connection import users_collection, blacklisted_tokens
from bson import ObjectId

SECRET_KEY = "SECRET_KEY_FOR_JWT_TOKENS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to validate JWT token and return current user.
    Checks if token is blacklisted and if user exists.
    """
    try:
        # Check if token is blacklisted
        blacklisted = await blacklisted_tokens.find_one({"token": token})
        if blacklisted:
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Find user in DB
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Convert ObjectId to string for JSON serialization
        user["id"] = str(user["_id"])
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")