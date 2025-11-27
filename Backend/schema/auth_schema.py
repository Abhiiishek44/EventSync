from pydentic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class userBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None
    
class userRegister(userBase):  
    password:str= Field(...,min_length=6,example="strongpassword123")
    role: Optional[str] = Field("user", example="user")  # default role is 'user'



class UserLogin(BaseModel):
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
    
    
