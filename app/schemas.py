from pydantic import BaseModel
import datetime as dt
from typing import Optional
from typing import Union ,List,Dict # data types management

class ToolCallFunctions(BaseModel):
    name: str
    arguments: Union[str, Dict]

class ToolCall(BaseModel):
    id:str
    function: ToolCallFunctions

class Message(BaseModel):
   toolcalls: Optional[List[ToolCall]] = None 

class VapiRequest(BaseModel):
    message: Message

# The class itself VapiReqest will be calling message class which will
# call the other classes iteratively

class TodoResponse(BaseModel):
    title:str
    description: Union[str,None]
    completed: bool

    class Config:
        orm_model = True

class ReminderResponse(BaseModel):
    reminder_text:str
    importance: str

    class Config:
        orm_model = True


class CalenderEventResponse(BaseModel):
    title:str
    description: Union[str,None]
    event_from: dt.datetime
    event_to: dt.datetime

    class Config:
        orm_model = True 