from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from schema.auth_schema import userLogin, userRegister
from database.connection import blacklisted_tokens
from controller.auth_controller import login_user, register_user, get_user_by_id, delete_user


router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    await blacklisted_tokens.insert_one({"token": token})
    return {"message": "Logged out successfully"}

@router.post("/register")
async def register(user: userRegister):
    return await register_user(user)


@router.post("/login")
async def login(user: userLogin):
    return await login_user(user)

@router.get("/{user_id}")
async def get_user(user_id: str):
    return await get_user_by_id(user_id)

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    return await delete_user(user_id)