import json
import datetime as dt
from typing import Union # data types management

from pydantic import BaseModel 

from fastapi import FastAPI,HTTPException,Depends
from fastapi.requests import Request 

from sqlalchemy import create_engine,Column,String,Boolean,Integer,DateTime
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base

# configuring sql database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

app = FastAPI()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True,index=True)
    tittle = Column(String,index=True) #By default it will filled as not null
    description = Column(String,nullable=True)
    completed  = Column(Boolean,default=False)

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer,primary_key=True,index=True)
    reminder_text = Column(String) #By default it will filled as not null
    importance = Column(String,nullable=True)

class CalenderEvent(Base):
    __tablename__ = 'calender_events'
    id = Column(Integer,primary_key=True,index=True)
    tittle = Column(String,index=True) #By default it will filled as not null
    description = Column(String,nullable=True)
    event_from = Column(DateTime)
    event_to = Column(DateTime)


Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

class ToolCallFunctions(BaseModel):
    name: str
    arguments: str | dict

class ToolCall(BaseModel):
    id:str
    function: ToolCallFunctions

class Message(BaseModel):
    toolcalls: list[ToolCall]

class VapiRequest(BaseModel):
    message: Message

# The class itself VapiReqest will be calling message class which will
# call the other classes iteratively

class TodoResponse(BaseModel):
    id: int
    title:str
    description: Union[str,None]
    completed: bool

    class Config:
        orm_model = True

class ReminderResponse(BaseModel):
    id: int
    reminder_text:str
    importance: str

    class Config:
        orm_model = True


class CalenderEventResponse(BaseModel):
    id: int
    title:str
    description: Union[str,None]
    event_from: dt.datetime
    event_to: dt.datetime

    class Config:
        orm_model = True
# Amazing thing about VAPI is that anything has to be a post request

@app.post("/create_todo/")
def create_todo(request:VapiRequest,db:Session = Depends(get_db)):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == 'createTodo':
            args = tool_call.function.arguments
            break
    else:
        HTTPException(status_code=400,detail="Invalid Request")

    if isinstance(args,str):
        args = json.loads(args)

    else:
        # Todo handle parsing if the result is not json
        pass
    tittle = args.get('title',"")
    description = args.get('description',"")

    todo = Todo(tittle= tittle,description=description)
    db.add(todo)
    db.commit()
    db.refresh() #NOTE: try without

    return {
        "result":[
            {
                "toolcallId":tool_call.id,
                "result": "sucess"
            }
        ]
    }

@app.post("/get_todos/")
def get_todos(request:VapiRequest,db:Session=Depends(get_db)):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == 'getTodos':
            todos= db.query(Todo).all()            
            return {
            "result":[
            {
                "toolcallId":tool_call.id,
                "result": [TodoResponse.from_orm(todo).dict() for todo in todos]
            }
             ]
             }
        
    else:
        HTTPException(status_code=400,detail="Invalid Request")
@app.post("/complete_todo/")
def complete_todo(request: VapiRequest,db :Session = Depends(get_db)):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == 'completeTodo':
            args = tool_call.function.arguments
            break

    else:
        HTTPException(status_code=400,detail="Invalid Request")

    if isinstance(args,str):
        args = json.loads(args)
    

    else:
        # Todo handle parsing if the result is not json
        pass
    
    todo_id = args.get("id")
    if not todo_id:

        raise HTTPException(status_code=400,detail="Missing To-Do Id")
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    
    todo.completed = True

    db.commit()
    db.refresh() #NOTE: try without

    return {
        "result":[
            {
                "toolcallId":tool_call.id,
                "result": "sucess"
            }
        ]
    }

@app.post("/delete_todo")
def delete_todo(request: VapiRequest,db:Session=Depends(get_db)):
    for tool_call in request.message.toolcalls:
        if tool_call.function.name == 'deleteTodo':
            args = tool_call.function.arguments
            break

    else:
        HTTPException(status_code=400,detail="Invalid Request")

    if isinstance(args,str):
        args = json.loads(args)
    

    else:
        # Todo handle parsing if the result is not json
        pass
    
    todo_id = args.get("id")
    if not todo_id:

        raise HTTPException(status_code=400,detail="Missing To-Do Id")
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    
    db.delete(todo)

    db.commit()
    # db.refresh() #NOTE: try without

    return {
        "result":[
            {
                "toolcallId":tool_call.id,
                "result": "sucess"
            }
        ]
    }
