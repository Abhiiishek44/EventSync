from controller.notice_controller import create_notice, get_notices_for_user, get_notice_by_id, update_notice, delete_notice
from fastapi import APIRouter, HTTPException, status, Depends
from schema.notice_schema import NoticeCreate, NoticeResponse, NoticeUpdate
from jwt_auth.jwt_handler import get_current_user


router = APIRouter(
    prefix="/notices",
    tags=["notices"]
)

@router.post("/", response_model=NoticeResponse)
async def create_notice_endpoint(notice: NoticeCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    return await create_notice(notice, user_id) 




@router.get("/", response_model=list[NoticeResponse])
async def get_notices_endpoint(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    return await get_notices_for_user(user_id)



@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice_endpoint(notice_id: str):
    notice = await get_notice_by_id(notice_id)
    if notice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")
    return notice   



@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice_endpoint(notice_id: str, notice: NoticeUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    updated_notice = await update_notice(notice_id, notice, user_id)
    if updated_notice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")
    return updated_notice




@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notice_endpoint(notice_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deleted = await delete_notice(notice_id, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")
    
    

