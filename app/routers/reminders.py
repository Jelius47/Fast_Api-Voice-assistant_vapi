from fastapi import APIRouter, Depends, HTTPException
import json
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..models import Reminder
from .todos import process_toolcall

router = APIRouter( tags=["todos"])

@router.post("/add_reminder/", response_model=schemas.ReminderResponse)
def add_reminder(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "addReminder")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    todo_data = {
        "reminder_text" :args.get("reminder_text"),
        "importance" : args.get("importance")
    }
    
    reminder = crud.create_todo(db, todo_data)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": schemas.ReminderResponse.model_validate(reminder).model_dump()
        }]
    }

@router.post("/get_reminders/",response_model=schemas.ReminderResponse)
def get_reminders(request:schemas.VapiRequest,db: Session=Depends(get_db)):
    tool_call = process_toolcall(request,"getReminders")
    reminders = crud.get_reminders(db=db)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": [schemas.ReminderResponse.model_validate(reminder).model_dump() for reminder in reminders]
        }]
    }
   

@router.post("/delete_reminder/",response_model=schemas.ReminderResponse)
def delete_reminder(request: schemas.VapiRequest,db:Session=Depends(get_db)):
    tool_call = process_toolcall(request, "deleteReminder")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    reminder_id = args.get("id")
    if not reminder_id:
        raise HTTPException(status_code=400, detail="Missing reminder ID")
    
    reminder = crud.delete_reminder(db, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": {"id": reminder_id, "deleted": True}
        }]
    }