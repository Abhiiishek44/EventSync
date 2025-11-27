from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime, date
from typing import List

class NoticeBase(BaseModel):
    title: str = Field(..., example="Important Notice")
    content: str = Field(..., example="This is the content of the notice.")
    start_date: Optional[datetime] = Field(None, example="2024-01-01T00:00:00")
    end_date: Optional[datetime] = Field(None, example="2024-01-31T23:59:59")
    audience: Optional[str] = Field(None, example="all")  # e.g., all, students, faculty
    priority: Optional[int] = Field(1, example=1)  # e.g., 1 (high), 2 (medium), 3 (low)




class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    audience: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    attachments: Optional[List[HttpUrl]] = None
    is_published: Optional[bool] = None
    is_important: Optional[bool] = None
    priority: Optional[int] = None
    
    
class NoticeResponse(NoticeBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
