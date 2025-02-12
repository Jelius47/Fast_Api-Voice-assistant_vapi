from fastapi import FastAPI
from .routers import todos, reminders, calender
from .database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)
app.include_router(reminders.router)
app.include_router(calender.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def read_root():
    return {"message": "Voice Assistant API"}