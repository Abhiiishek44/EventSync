from fastapi import APIRouter, Depends
from schema.teacher_schema import TeacherCreate, TeacherResponse
from controller.admin.teacher_controller import (
    create_teacher,
    get_all_teachers,
    get_teacher_by_id,
    delete_teacher
)
from jwt_auth.dependency import get_current_admin


router = APIRouter(
    prefix="/admin/teachers",
    tags=["admin-teachers"]
)


@router.post("/", response_model=TeacherResponse)
async def create_teacher_endpoint(
    teacher: TeacherCreate,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Create a new teacher account (Admin only).
    
    - Generates unique teacher ID and secure password
    - Sends login credentials to teacher's email
    - Requires admin authentication
    """
    admin_id = str(current_admin["_id"])
    return await create_teacher(teacher, admin_id)


@router.get("/", response_model=list[TeacherResponse])
async def get_teachers_endpoint(current_admin: dict = Depends(get_current_admin)):
    """
    Get all teachers (Admin only).
    
    - Returns list of all registered teachers
    - Requires admin authentication
    """
    return await get_all_teachers()


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_endpoint(
    teacher_id: str,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Get a specific teacher by ID (Admin only).
    
    - Returns teacher details
    - Requires admin authentication
    """
    return await get_teacher_by_id(teacher_id)


@router.delete("/{teacher_id}")
async def delete_teacher_endpoint(
    teacher_id: str,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Delete a teacher account (Admin only).
    
    - Permanently removes teacher account
    - Requires admin authentication
    """
    admin_id = str(current_admin["_id"])
    return await delete_teacher(teacher_id, admin_id)
