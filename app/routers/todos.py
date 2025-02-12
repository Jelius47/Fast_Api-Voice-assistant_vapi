from fastapi import APIRouter, Depends, HTTPException
import json
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter( tags=["todos"])

def process_toolcall(request: schemas.VapiRequest, function_name: str):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == function_name:
            return tool_call
    raise HTTPException(status_code=400, detail="Invalid Request")

@router.post("/create_todo/", response_model=schemas.VapiRequest)
def create_todo(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "createTodo")
    args = tool_call.function.arguments
    
    if isinstance(args, str):
        args = json.loads(args)
    
    todo_data = {
        "title": args.get("title", ""),
        "description": args.get("description", "")
    }
    
    todo = crud.create_todo(db, todo_data)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": schemas.TodoResponse.from_orm(todo).dict()
        }]
    }

@router.post("/get_todos/", response_model=schemas.VapiRequest)
def get_todos(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = process_toolcall(request, "getTodos")
    todos = crud.get_todos(db)
    return {
        "result": [{
            "toolcallId": tool_call.id,
            "result": [schemas.TodoResponse.from_orm(todo).dict() for todo in todos]
        }]
    }

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

@router.post("/delete_todo/", response_model=schemas.VapiRequest)
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