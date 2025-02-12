from pydantic import BaseModel
import datetime as dt
from typing import Optional
from typing import Union # data types management

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