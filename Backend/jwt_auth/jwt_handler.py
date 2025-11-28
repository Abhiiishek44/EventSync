from datetime import datetime, timedelta
from jose import jwt
import os 
from fastapi import HTTPException
from database.connection import users_collection
from bson import ObjectId

SECRET_KEY = "SECRET_KEY_FOR_JWT_TOKENS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(id: str)-> str:
    to_encode = {"id": id}
    expire= datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def decode_access_token(token: str) -> dict:
    try:
        # decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # find user in DB
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")