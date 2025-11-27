from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class attendenceBase(BaseModel):
    event_id: int = Field(..., description="The ID of the event")
    user_id: int = Field(..., description="The ID of the user")
    status: str = Field(..., example="present")  # e.g., present, absent, late
    attendance_date: datetime = Field(..., example="2024-05-15T10:00:00")
    remarks: Optional[str] = Field(None, example="Arrived late due to traffic")

class AttendanceCreate(attendenceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

class AttendanceResponse(attendenceBase):
    id: int
    created_at: datetime
    updated_at: datetime   
