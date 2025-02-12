from fastapi import FastAPI
from .routers import todos, reminders, calender
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)
app.include_router(reminders.router)
app.include_router(calender.router)

@app.post("/")
def read_root():
    return {"message": "Voice Assistant API"}