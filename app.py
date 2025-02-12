# import json
# import datetime as dt
# from typing import Union # data types management

# from pydantic import BaseModel 

# from fastapi import FastAPI,HTTPException,Depends
# from fastapi.requests import Request 

# from sqlalchemy import create_engine,Column,String,Boolean,Integer,DateTime
# from sqlalchemy.orm import sessionmaker,Session
# from sqlalchemy.ext.declarative import declarative_base

# # configuring sql database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()

# app = FastAPI()

# class Todo(Base):
#     __tablename__ = 'todos'
#     id = Column(Integer,primary_key=True,index=True)
#     tittle = Column(String,index=True) #By default it will filled as not null
#     description = Column(String,nullable=True)
#     completed  = Column(Boolean,default=False)

# class Reminder(Base):
#     __tablename__ = 'reminders'
#     id = Column(Integer,primary_key=True,index=True)
#     reminder_text = Column(String) #By default it will filled as not null
#     importance = Column(String,nullable=True)

# class CalenderEvent(Base):
#     __tablename__ = 'calender_events'
#     id = Column(Integer,primary_key=True,index=True)
#     tittle = Column(String,index=True) #By default it will filled as not null
#     description = Column(String,nullable=True)
#     event_from = Column(DateTime)
#     event_to = Column(DateTime)


# Base.metadata.create_all(bind = engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db

#     finally:
#         db.close()

# class ToolCallFunctions(BaseModel):
#     name: str
#     arguments: str | dict

# class ToolCall(BaseModel):
#     id:str
#     function: ToolCallFunctions

# class Message(BaseModel):
#     toolcalls: list[ToolCall]

# class VapiRequest(BaseModel):
#     message: Message

# # The class itself VapiReqest will be calling message class which will
# # call the other classes iteratively

# class TodoResponse(BaseModel):
#     id: int
#     title:str
#     description: Union[str,None]
#     completed: bool

#     class Config:
#         orm_model = True

# class ReminderResponse(BaseModel):
#     id: int
#     reminder_text:str
#     importance: str

#     class Config:
#         orm_model = True


# class CalenderEventResponse(BaseModel):
#     id: int
#     title:str
#     description: Union[str,None]
#     event_from: dt.datetime
#     event_to: dt.datetime

#     class Config:
#         orm_model = True
# # Amazing thing about VAPI is that anything has to be a post request

# @app.post("/create_todo/")
# def create_todo(request:VapiRequest,db:Session = Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == 'createTodo':
#             args = tool_call.function.arguments
#             break
#     else:
#         HTTPException(status_code=400,detail="Invalid Request")

#     if isinstance(args,str):
#         args = json.loads(args)

#     else:
#         # Todo handle parsing if the result is not json
#         pass
#     tittle = args.get('title',"")
#     description = args.get('description',"")

#     todo = Todo(tittle= tittle,description=description)
#     db.add(todo)
#     db.commit()
#     db.refresh() #NOTE: try without

#     return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": "sucess"
#             }
#         ]
#     }

# @app.post("/get_todos/")
# def get_todos(request:VapiRequest,db:Session=Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == 'getTodos':
#             todos= db.query(Todo).all()            
#             return {
#             "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": [TodoResponse.from_orm(todo).dict() for todo in todos]
#             }
#              ]
#              }
        
#     else:
#         HTTPException(status_code=400,detail="Invalid Request")
        
# @app.post("/complete_todo/")
# def complete_todo(request: VapiRequest,db :Session = Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == 'completeTodo':
#             args = tool_call.function.arguments
#             break

#     else:
#         HTTPException(status_code=400,detail="Invalid Request")

#     if isinstance(args,str):
#         args = json.loads(args)
    

#     else:
#         # Todo handle parsing if the result is not json
#         pass
    
#     todo_id = args.get("id")
#     if not todo_id:

#         raise HTTPException(status_code=400,detail="Missing To-Do Id")
#     todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(status_code=404,detail="Todo not found")
    
#     todo.completed = True

#     db.commit()
#     db.refresh() #NOTE: try without

#     return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": "sucess"
#             }
#         ]
#     }

# @app.post("/delete_todo")
# def delete_todo(request: VapiRequest,db:Session=Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == 'deleteTodo':
#             args = tool_call.function.arguments
#             break

#     else:
#         HTTPException(status_code=400,detail="Invalid Request")

#     if isinstance(args,str):
#         args = json.loads(args)
    

#     else:
#         # Todo handle parsing if the result is not json
#         pass
    
#     todo_id = args.get("id")
#     if not todo_id:

#         raise HTTPException(status_code=400,detail="Missing To-Do Id")
#     todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if not todo:
#         raise HTTPException(status_code=404,detail="Todo not found")
    
#     db.delete(todo)

#     db.commit()
#     # db.refresh() #NOTE: try without

#     return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": "sucess"
#             }
#         ]
#     }
# @app.post("/add_reminder/")
# def add_reminder(request : VapiRequest,db: Session = Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "addReminder":
#             args = tool_call.function.arguments

#             if isinstance(args,str):
#                 args = json.loads(args)
#             reminder_text = args.get("reminder_text")
#             importance = args.get("importance")

#             if not reminder_text or not importance:
#                 raise HTTPException(status_code=400,detail="Missing the required fields")

#             reminder = Reminder(reminder_text= reminder_text,importance=importance)
#             db.add(reminder)
#             db.commit()
#             db.refresh(reminder)

#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": ReminderResponse.from_orm(reminder).dict()
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid request")

# @app.post("/get_reminders/")
# def get_reminers(request:VapiRequest,db: Session=Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "getReminders":
#             reminders = db.query(Reminder).all()
#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": [ReminderResponse.from_orm(reminder).dict() for reminder in reminders]
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid request")

# @app.post("/delete_reminder/")
# def delete_reminder(request: VapiRequest,db:Session=Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "deleteReminder":
#             args  = tool_call.function.arguments
#             if isinstance(args,str):
#                 args = json.loads(args)
#             reminder_id = args.get("id")
            
#             if not reminder_id:
#                 raise HTTPException(status_code=400,detail="Missing reminder ID")
#             reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()

#             if not reminder:
#                 raise HTTPException(status_code=400,detail="Reminder not found")
            
#             db.delete(reminder)
#             db.commit()
#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": {"id":reminder_id,"deleted":True}
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid Request")

# @app.post("/add_calender_entry/")
# def add_callender_entry(request: VapiRequest,db:Session=Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "addCalenderEntry":
#             args = tool_call.function.arguments

#             if isinstance(args,str):
#                 args = json.loads(args)
#             title = args.get("tittle",'')
#             description = args.get("description",'')
#             event_from_str = args.get("event_from",'')
#             event_to_str = args.get("event_to",'')


#             if not title or not description or not event_from_str or not event_to_str:
#                 raise HTTPException(status_code=400,detail="Missing the required fields")
#             try:
#                 event_from = dt.datetime.fromisoformat(event_from_str)
#                 event_to = dt.datetime.fromisoformat(event_to_str)
#             except ValueError:
#                 raise HTTPException(status_code=400,detail="Invalid date format.Use ISO format")
            
#             callender_event = CalenderEvent(
#                 title = title,
#                 description = description,
#                 event_from = event_from,
#                 event_to = event_to
#             )
 
#             db.add(callender_event)
#             db.commit()
#             db.refresh(callender_event)

#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": ReminderResponse.from_orm(callender_event).dict()
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid request")


# @app.post("/get_calender_entries/")
# def get_callender_entries(request : VapiRequest,db: Session = Depends(get_db)):
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "getCalenderEntries":
#             events = db.query(CalenderEvent).all()
#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": [CalenderEventResponse.from_orm(event).dict() for event in events]
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid request")

# @app.post("/delete_calender_entry/")
# def delete_calender_entry(request:VapiRequest,db:Session=Depends(get_db)):        
#     for tool_call in request.message.toolcalls:
#         if tool_call.function.name == "deleteCalenderEntry":
#             args  = tool_call.function.arguments
#             if isinstance(args,str):
#                 args = json.loads(args)
#             event_id = args.get("id")
            
#             if not event_id:
#                 raise HTTPException(status_code=400,detail="Missing reminder ID")
#             event = db.query(CalenderEvent).filter(CalenderEvent.id == event_id).first()

#             if not event:
#                 raise HTTPException(status_code=400,detail="Reminder not found")
            
#             db.delete(event)
#             db.commit()
#             return {
#         "result":[
#             {
#                 "toolcallId":tool_call.id,
#                 "result": {"id":event_id,"deleted":True}
#             }
#         ]
#     }
#     raise HTTPException(status_code=400,detail="Invalid Request")
