from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class TeacherBase(BaseModel):
    name: str = Field(..., example="Dr. John Smith")
    email: EmailStr = Field(..., example="john.smith@university.edu")
    department: str = Field(..., example="Computer Science")
    subject: Optional[str] = Field(None, example="Data Structures")
    phone: Optional[str] = Field(None, example="+1234567890")
    role: str = Field(..., example="teacher")
    
    
class TeacherCreate(TeacherBase):
    """Schema for admin to create a teacher - password will be auto-generated"""
    pass


class TeacherResponse(TeacherBase):
    id: str
    teacher_id: str  # Generated unique teacher ID (e.g., TCH001)
    role: str
    is_active: bool
    created_at: datetime
    created_by: str  # Admin who created this teacher


class TeacherCredentials(BaseModel):
    """Credentials sent to teacher via email"""
    teacher_id: str
    password: str
    email: EmailStr
    role: str
    login_url: str = "http://localhost:8000/auth/login"
