from schema.auth_schema import userLogin , userRegister , UserResponse, hash_password, verify_password
from fastapi import HTTPException
from jwt_auth.jwt_handler import create_access_token
from bson import ObjectId
from datetime import datetime
from database.connection import users_collection



# ===================== Register User =====================

async def register_user(user: userRegister) -> UserResponse:
    new_user = user.dict()

    # Check if email exists
    existing_user = await users_collection.find_one({"email": new_user["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user["is_active"] = True
    new_user["created_at"] = datetime.utcnow()
    new_user["password"] = hash_password(new_user["password"])
    new_user["role"] = new_user.get("role", "student")  # safe default

    # Insert user
    result = await users_collection.insert_one(new_user)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to register user")

    created_user = await users_collection.find_one({"_id": result.inserted_id})

    # Remove sensitive values
    created_user["id"] = str(created_user["_id"])
    created_user.pop("_id", None)
    created_user.pop("password", None)

    return UserResponse(**created_user)


# ===================== Login User =====================

async def login_user(user: userLogin) -> dict:
    existing_user = await users_collection.find_one({"email": user.email})

    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    role = existing_user.get("role", "student")

    token = create_access_token({
        "id": str(existing_user["_id"]),
        "email": existing_user["email"],
        "role": role
    })

    return {"access_token": token, "token_type": "bearer"}


# ===================== Get User by ID =====================

async def get_user_by_id(user_id: str) -> UserResponse:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["id"] = str(user["_id"])
    user.pop("_id", None)
    user.pop("password", None)  # remove password before returning

    return UserResponse(**user)


# ===================== Delete User =====================

async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted successfully"}