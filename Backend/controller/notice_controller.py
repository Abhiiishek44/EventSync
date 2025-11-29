from schema.notice_schema import NoticeCreate, NoticeUpdate
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from database.connection import notices_collection  # MUST USE NOTICE COLLECTION


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
        "created_by": notice.get("created_by"),
        "created_at": notice.get("created_at"),
        "updated_at": notice.get("updated_at"),
    }


# ================= Create Notice ====================

async def create_notice(request: NoticeCreate, user_id: str):
    new_notice = request.dict()
    new_notice["created_by"] = user_id
    new_notice["created_at"] = datetime.utcnow()

    result = await notices_collection.insert_one(new_notice)
    created_notice = await notices_collection.find_one({"_id": result.inserted_id})

    return notice_serializer(created_notice)


# ================= Fetch all Notices ====================

async def get_all_notices():
    notices = []
    cursor = notices_collection.find({})
    async for document in cursor:
        notices.append(notice_serializer(document))
    return notices


# ================= Fetch Notice by ID ====================

async def get_notice_by_id(notice_id: str):
    notice = await notices_collection.find_one({"_id": ObjectId(notice_id)})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice_serializer(notice)


# ================= Update Notice ====================

async def update_notice(notice_id: str, request: NoticeUpdate, user_id: str):
    notice = await notices_collection.find_one({"_id": ObjectId(notice_id)})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if notice["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="You cannot update this notice")

    updated_data = {k: v for k, v in request.dict().items() if v is not None}
    updated_data["updated_at"] = datetime.utcnow()

    await notices_collection.update_one(
        {"_id": ObjectId(notice_id)},
        {"$set": updated_data}
    )

    updated_notice = await notices_collection.find_one({"_id": ObjectId(notice_id)})
    return notice_serializer(updated_notice)


# ================= Delete Notice ====================

async def delete_notice(notice_id: str, user_id: str):
    notice = await notices_collection.find_one({"_id": ObjectId(notice_id)})
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if notice["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this notice")

    result = await notices_collection.delete_one({"_id": ObjectId(notice_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete notice")

    return {"detail": "Notice deleted successfully"}
