from fastapi import APIRouter, Depends, HTTPException
import json
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from .todos import process_toolcall

router = APIRouter( tags=["todos"])

@router.post("/add_calender_entry/",response_model=schemas.VapiRequest)
def add_callender_entry(request: schemas.VapiRequest,db:Session=Depends(get_db)):
    tool_call = process_toolcall(request, "addCalenderEntry")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    event_data = {
        "title" : args.get("tittle",''),
        "description"  : args.get("description",''),
        "event_from_str" : args.get("event_from",''),
        "event_to_str" : args.get("event_to",'')
    }
    
    event = crud.create_calendar_event(db, event_data=event_data)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": schemas.CalenderEventResponse.from_orm(event).dict()
        }]
    }


@router.post("/get_calender_entries/",response_model=schemas.VapiRequest)
def get_callender_entries(request : schemas.VapiRequest,db: Session = Depends(get_db)):

    tool_call = process_toolcall(request,"getCalenderEntries")
    calenders = crud.get_calendar_events(db=db)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": [schemas.ReminderResponse.from_orm(calender).dict() for calender in calenders]
        }]
    }

@router.post("/delete_calender_entry/",response_model=schemas.VapiRequest)
def delete_calender_entry(request:schemas.VapiRequest,db:Session=Depends(get_db)):        
    tool_call = process_toolcall(request, "deleteCalenderEntry")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    event_id = args.get("id")
    if not event_id:
        raise HTTPException(status_code=400, detail="Missing Calender event ID")
    
    event = crud.delete_calendar_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event  not found")
    
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": {"id": event_id, "deleted": True}
        }]
    }
    