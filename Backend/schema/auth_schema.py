from typing import Optional
from datetime import datetime
import bcrypt
from pydantic import BaseModel, Field, EmailStr

class userBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None
    
class userRegister(userBase):  
    password:str= Field(...,min_length=6,example="strongpassword123")
    role: Optional[str] = Field("user", example="user")  # default role is 'user'



class userLogin(BaseModel):
    email: EmailStr = Field(...,example="user@example.com")
    password: str = Field(...,min_length=6,example="strongpassword123")
    


class userUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None
    password: Optional[str] = Field(None, min_length=6, example="newstrongpassword123")
    
class userRoleUpdate(BaseModel):
    role: str = Field(...,example="admin")
    
class UserResponse(userBase):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime


class token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    
    
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))