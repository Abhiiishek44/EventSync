from fastapi import APIRouter, HTTPException, status
from schema.event_schema import EventCreate, EventResponse, EventUpdate
from controller.event_controller import(
    create_event,
    get_all_events,
    get_event_by_id,
    update_event,
    delete_event
)


router = APIRouter(
    prefix="/events",
    tags=["events"]
) 



@router.post("/", response_model=EventResponse)
async def create_event_endpoint(event: EventCreate, user_id: str):
    return await create_event(event, user_id) 


@router.get("/", response_model=list[EventResponse])
async def get_events_endpoint():
    return await get_all_events()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_endpoint(event_id: str):
    event = await get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(event_id: str, event: EventUpdate,user_id: str):
    updated_event = await update_event(event_id, event,user_id)
    if updated_event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return updated_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_endpoint(event_id: str, user_id: str):
    await delete_event(event_id, user_id)
    return None