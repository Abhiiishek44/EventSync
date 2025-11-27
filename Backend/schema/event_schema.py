from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,date



class EventBase ( BaseModel ):
    title : str = Field ( ... , example = "Annual Meeting" )
    description : str = Field ( ... , example = "Description of the event." )
    event_date : datetime = Field ( ... , example = "2024-05-15T10:00:00" )
    location :  str = Field ( ... , example = "Conference Hall A" )
    tags: Optional [ str ] = Field ( None , example = "meeting,annual" )
    organizer : Optional [ str ] = Field ( None , example = "John Doe" )
    audience : Optional [ str ] = Field ( None , example = "all" )  # e.g., all, members, guests
    start_time : Optional [ datetime ] = Field ( None , example = "2024-05-15T10:00:00" )
    end_time : Optional [ datetime ] = Field ( None , example = "2024-05-15T12:00:00" )
    start_date : Optional [ datetime ] = Field ( None , example = "2024-05-01T00:00:00" )
    end_date : Optional [ datetime ] = Field ( None , example = "2024-05-31T23:59:59" )
  
  
class EventCreate(EventBase):
    pass
    

class EventUpdate ( BaseModel ):
    title : Optional [ str ] = None
    description : Optional [ str ] = None
    event_date : Optional [ date ] = None
    location : Optional [ str ] = None
    organizer : Optional [ str ] = None
    start_time : Optional [ datetime ] = None
    end_time : Optional [ datetime ] = None
    audience : Optional [ str ] = None
    
class EventResponse ( EventBase ):
    id : str
    created_at : datetime
    updated_at : Optional[datetime] = None
