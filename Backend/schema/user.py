from pydentic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None 
    

class userRegister(UserBase):
    password:str= Field(...,min_length=6,example="strongpassword123")
    

class userLogin(BaseModel):
    email: EmailStr = Field(...,example="user@example.com")
    password: str = Field(...,min_length=6,example="strongpassword123")
    
class userRoleUpdate(BaseModel):
    role: str = Field(...,example="admin")
    
class UserResponse(UserBase):
    id: int
    name: str
    email: EmailStr
    department: Optional[str]
    year: Optional[int]
    role: str
    is_active: bool
    created_at: datetime