from datetime import datetime
from http.client import HTTPException
from database.connection import events_collection
from schema.event_schema import EventCreate, EventUpdate



def event_serializer(event) -> dict:
    return {
        "id": str(event["_id"]),
        "title": event["title"],
        "description": event["description"],
        "event_date": event["event_date"],
        "location": event["location"],
        "tags": event.get("tags"),
        "organizer": event.get("organizer"),
        "audience": event.get("audience"),
        "start_time": event.get("start_time"),
        "end_time": event.get("end_time"),
        "start_date": event.get("start_date"),
        "end_date": event.get("end_date"),
        "organizer": event.get("organizer"),
        "created_at": event["created_at"],
        "updated_at": event.get("updated_at"),
    }

async def create_event(request: EventCreate, user_id: str):
          new_event = request.dict() 
          new_event['organizer'] = user_id
          new_event['created_at'] = datetime.utcnow()
        
          result = await events_collection.insert_one(new_event)
          created_event = await events_collection.find_one({"_id": result.inserted_id})
          created_event = event_serializer(created_event)
          return created_event    
    
async def get_all_events():
          events = []
          cursor = events_collection.find({})
          async for document in cursor:
              document['id'] = str(document['_id'])
              events.append(document)
          return events 
    
async def get_event_by_id(event_id: str):
            event = await events_collection.find_one({"_id": event_id})
            if not event:
                 raise HTTPException(status_code=404, detail="Event not found")
            return event_serializer(event)


async def update_event(event_id: str, request: EventUpdate, user_id: str):
          event = await events_collection.find_one({"_id": event_id})
          if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            
          if event["organizer"] != user_id:
            raise HTTPException(status_code=403, detail="You cannot update this event")
    
          updated_data = {k: v for k, v in request.dict().items() if v is not None}
          if updated_data:
                updated_data["updated_at"] = datetime.utcnow()
                await events_collection.update_one(
                    {"_id": event_id},
                    {"$set": updated_data}
                )
          update_event = await events_collection.find_one({"_id": event_id})
          return event_serializer(update_event)
      

async def delete_event(event_id: str, user_id: str):
            event = await events_collection.find_one({"_id": event_id})
            if not event:
                    raise HTTPException(status_code=404, detail="Event not found")
                
            if  event["organizer"] != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this event")
            await events_collection.delete_one({"_id": event_id})
            return {"detail": "Event deleted successfully"}

