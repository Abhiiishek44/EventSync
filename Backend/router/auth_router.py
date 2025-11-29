from fastapi import APIRouter, Depends
from schema.auth_schema import userLogin, userRegister, token
from database.connection import blacklisted_tokens
from controller.auth_controller import login_user, register_user, get_user_by_id, delete_user
from jwt_auth.jwt_handler import get_current_user, oauth2_scheme
from fastapi import HTTPException

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post("/register")
async def register(user: userRegister):
    return await register_user(user)


@router.post("/login", response_model=token)
async def login(user: userLogin):
    return await login_user(user)


@router.post("/logout")
async def logout(token_str: str = Depends(oauth2_scheme), current_user: dict = Depends(get_current_user)):
    await blacklisted_tokens.insert_one({"token": token_str})
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if user_id != str(current_user["_id"]):
        raise HTTPException(403, "You cannot access other users' profile")

    return await get_user_by_id(user_id)

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str, current_user: dict = Depends(get_current_user)):
    if user_id != str(current_user["_id"]):
        raise HTTPException(403, "You cannot delete another user's account")

    return await delete_user(user_id)

