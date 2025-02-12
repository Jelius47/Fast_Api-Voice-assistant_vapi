from fastapi import APIRouter, Depends, HTTPException
import json
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter( tags=["todos"])

def process_toolcall(request: schemas.VapiRequest, function_name: str):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == function_name:
            return tool_call
    raise HTTPException(status_code=400, detail="Invalid Request")

@router.post("/create_todo/")
async def create_todo(request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()  # Get the raw JSON payload
    logging.info(f"Received raw request: {raw_body.decode('utf-8')}")  # Log it
    
    parsed_body = await request.json()  # Parse the JSON
    logging.info(f"Parsed request body: {parsed_body}")  # Log parsed JSON
    
    request_obj = schemas.VapiRequest(**parsed_body)  # Validate against schema

    tool_call = process_toolcall(request_obj, "createTodo")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    todo_data = {
        "title": args.get("title", ""),
        "description": args.get("description", "")
    }
    
    if not todo_data["title"]:
        raise HTTPException(status_code=400, detail="Missing title")
    
    todo = crud.create_todo(db, todo_data)

    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": schemas.TodoResponse.model_validate(todo).model_dump()
        }]
    }

@router.post("/get_todos/")
def get_todos(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "getTodos")
    todos = crud.get_todos(db)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": [schemas.TodoResponse.model_validate(todo).model_dump() for todo in todos]
        }]
    }

@router.post("/complete_todo/")
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
            "result": schemas.TodoResponse.model_validate(todo).model_dump()
        }]
    }

@router.post("/delete_todo/")
def delete_todo(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "deleteTodo")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    todo_id = args.get("id")
    if not todo_id:
        raise HTTPException(status_code=400, detail="Missing todo ID")
    
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": {"id": todo_id, "deleted": True}
        }]
    }