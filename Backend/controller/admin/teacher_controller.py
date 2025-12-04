from fastapi import HTTPException
from database.connection import teachers_collection, users_collection
from schema.teacher_schema import TeacherCreate, TeacherResponse
from schema.auth_schema import hash_password
from utils.email_util import send_teacher_credentials_email
from datetime import datetime
from bson import ObjectId
import secrets
import string


def generate_teacher_id() -> str:
    """
    Generate a unique teacher ID in format TCH001, TCH002, etc.
    """
    # Get the count of existing teachers
    import asyncio
    
    async def get_count():
        count = await teachers_collection.count_documents({})
        return count
    
    try:
        loop = asyncio.get_event_loop()
        count = loop.run_until_complete(get_count())
    except RuntimeError:
        # If no event loop is running, create one
        count = asyncio.run(get_count())
    
    # Generate ID with zero padding
    teacher_number = count + 1
    return f"TCH{teacher_number:03d}"


def generate_random_password(length: int = 12) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Length of the password (default 12)
        
    Returns:
        str: Randomly generated password
    """
    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]
    
    password += [secrets.choice(characters) for _ in range(length - 4)]
   
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


async def create_teacher(teacher_data: TeacherCreate, admin_id: str) -> TeacherResponse:
    """
    Create a new teacher account with auto-generated credentials.
    Sends login credentials to teacher's email.
    
    Args:
        teacher_data: Teacher information from request
        admin_id: ID of the admin creating the teacher
        
    Returns:
        TeacherResponse: Created teacher information
        
    Raises:
        HTTPException: If email already exists or creation fails
    """
    
    # Check if email already exists in teachers collection
    existing_teacher = await teachers_collection.find_one({"email": teacher_data.email})
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher with this email already exists")
    
    # Check if email exists in users collection
    existing_user = await users_collection.find_one({"email": teacher_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="This email is already registered as a user")
    
    teacher_id = generate_teacher_id()
    password = generate_random_password()
    
    hashed_password = hash_password(password)
    
    # Prepare teacher document
    new_teacher = {
        "name": teacher_data.name,
        "email": teacher_data.email,
        "department": teacher_data.department,
        "subject": teacher_data.subject,
        "phone": teacher_data.phone,
        "teacher_id": teacher_id,
        "password": hashed_password,
        "role": teacher_data.role,
    }
    
    # Insert into database
    result = await teachers_collection.insert_one(new_teacher)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create teacher account")
    
    # Send credentials via email
    email_sent = send_teacher_credentials_email(
        to_email=teacher_data.email,
        teacher_name=teacher_data.name,
        teacher_id=teacher_id,
        password=password,
        role=teacher_data.role
    )
    
    if not email_sent:
        # Log warning but don't fail the request
        print(f"⚠️ Warning: Teacher created but email failed to send to {teacher_data.email}")
        print(f"📧 Manual credentials - Teacher ID: {teacher_id}, Password: {password}")
    
    # Fetch created teacher
    created_teacher = await teachers_collection.find_one({"_id": result.inserted_id})
    
    # Format response
    created_teacher["id"] = str(created_teacher["_id"])
    created_teacher.pop("_id", None)
    created_teacher.pop("password", None)  # Don't return password in response
    
    return TeacherResponse(**created_teacher)


async def get_all_teachers():
    """
    Get all teachers (admin only).
    
    Returns:
        list: List of all teachers
    """
    teachers = []
    cursor = teachers_collection.find({})
    
    async for teacher in cursor:
        teacher["id"] = str(teacher["_id"])
        teacher.pop("_id", None)
        teacher.pop("password", None) 
        teachers.append(teacher)
    
    return teachers


async def get_teacher_by_id(teacher_id: str) -> dict:
    """
    Get a specific teacher by their MongoDB ID.
    
    Args:
        teacher_id: MongoDB ObjectId as string
        
    Returns:
        dict: Teacher information
        
    Raises:
        HTTPException: If teacher not found
    """
    teacher = await teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher["id"] = str(teacher["_id"])
    teacher.pop("_id", None)
    teacher.pop("password", None)  # Don't expose password
    
    return teacher


async def delete_teacher(teacher_id: str, admin_id: str):
    """
    Delete a teacher account (admin only).
    
    Args:
        teacher_id: MongoDB ObjectId as string
        admin_id: ID of the admin performing deletion
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If teacher not found
    """
    result = await teachers_collection.delete_one({"_id": ObjectId(teacher_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return {"detail": f"Teacher account deleted successfully by admin {admin_id}"}
