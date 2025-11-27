from schema.notice_schema import NoticeCreate, NoticeUpdate
from datetime import datetime
from http.client import HTTPException
from database.connection import events_collection


def notice_serializer(notice) -> dict:
    return {
        "id": str(notice["_id"]),
        "title": notice["title"],
        "content": notice["content"],
        "start_date": notice.get("start_date"),
        "end_date": notice.get("end_date"),
        "audience": notice.get("audience"),
        "tags": notice.get("tags"),
        "priority": notice.get("priority"),
        "created_by": notice["created_by"],
        "created_at": notice["created_at"],
        "updated_at": notice.get("updated_at"),
    }


def create_notice(request: NoticeCreate, user_id: str):
    new_notice = request.dict()
    new_notice['created_by'] = user_id
    new_notice['created_at'] = datetime.utcnow()
    result = events_collection.insert_one(new_notice)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to create notice")
    created_notice = events_collection.find_one({"_id": result.inserted_id})
    created_notice = notice_serializer(created_notice)
    return created_notice


def get_all_notices():
    notices = []
    cursor = events_collection.find({})
    for document in cursor:
        document = notice_serializer(document)
        notices.append(document)
    return notices


def get_notice_by_id(notice_id: str):
    notice= events_collection.find_one({"_id": notice_id})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice_serializer(notice)

def update_notice(notice_id: str, request: NoticeUpdate, user_id: str):
    notice = events_collection.find_one({"_id": notice_id})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    if notice["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="You cannot update this notice")

    updated_data = {k: v for k, v in request.dict().items() if v is not None}
    if updated_data:
        updated_data["updated_at"] = datetime.utcnow()
        events_collection.update_one({"_id": notice_id}, {"$set": updated_data})

    updated_notice = events_collection.find_one({"_id": notice_id})
    return notice_serializer(updated_notice)


def delete_notice(notice_id: str, user_id: str):
    notice = events_collection.find_one({"_id": notice_id})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    if notice["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="You cannot delete this notice")
    delete_notice = events_collection.delete_one({"_id": notice_id})
    if delete_notice.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete notice")
    return {"detail": "Notice deleted successfully"}


