from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class RegistrationBase(BaseModel):
    event_id: int = Field(..., description="The ID of the event being registered for")
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    phone: Optional[str] = Field(None, max_length=15)
    department: Optional[str] = None
    year: Optional[str] = None             # e.g. "FE", "SE", "TE", "BE"
    
    
class createRegistration(RegistrationBase):
    pass
    
class RegistrationUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    
class RegistrationResponse(RegistrationBase):
    id: int
    created_at: datetime