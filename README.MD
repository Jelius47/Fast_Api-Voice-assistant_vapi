## Ai voice assisntant using vapi

A backend API for managing todos, reminders, and calendar events through voice commands using VAPI integration.
--Project directory structure 


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)


## Features

✅ **Todo Management**  
- Create new todos
-- Example route for todos

```bash
@router.post("/complete_todo/", response_model=schemas.VapiRequest)
def complete_todo(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "completeTodo")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    todo_id = args.get("id")
    if not todo_id:
        raise HTTPException(status_code=400, detail="Missing todo ID")
    
    todo = crud.complete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": schemas.TodoResponse.from_orm(todo).dict()
        }]
        }
```

- Retrieve all todos
- Mark todos as complete
- Delete todos

📅 **Calendar Events** :
--- Exampler route for calender 
```bash
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
```

⏰ **Reminders** 
--- Exampler route for reminders
```bash
@router.post("/get_reminders/",response_model=schemas.VapiRequest)
def get_reminders(request:schemas.VapiRequest,db: Session=Depends(get_db)):
    tool_call = process_toolcall(request,"getReminders")
    reminders = crud.get_reminders(db=db)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": [schemas.ReminderResponse.from_orm(reminder).dict() for reminder in reminders]
        }]
    }
```

- SQLite database integration
- VAPI-compatible request/response format
- Pydantic validation for all endpoints

---

## Installation

1. **Clone repository**:
```bash
git clone https://github.com/Jelius47/Fast_Api-Voice-assistant_vapi.git
cd Fast_Api-Voice-assistant_vapi
```
2. **create Virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Run the application**
```bash
uvicorn app.main:app --reload
```
--- Make sure you have ngrok running (good if its a static domain) as to expose it too the web or you can deploy it on either render and configure the endpoints at [vapi](https://dashboard.vapi.ai/assistants/813e6e4d-aaf9-4bfe-a602-28902076097a)
## API Endpoints
--- In [vapi](https://dashboard.vapi.ai/assistants/813e6e4d-aaf9-4bfe-a602-28902076097a) dashboard make sure 
the routes are `https://your-exposed-application/specified_route`


## Project structure
```bash
fastApi-Voice_ass/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app instance
│   ├── routers/         # API routers
│   │   ├── __init__.py
│   │   ├── todos.py
│   │   ├── reminders.py
│   │   └── calendar.py
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic models
│   ├── crud.py          # Database operations
│   └── database.py      # Database configuration
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```
## Contributing
Feel free to contribute,Happy codding
### Regards
Jelius H.
[NeuralNine](https://youtu.be/91fv7QIcZcQ) for more detailed tutorial