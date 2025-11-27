from pydentic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class userBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None
    
class userRegister(userBase):