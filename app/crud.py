from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Todo CRUD Operations
def create_todo(db: Session, todo_data: dict):
    todo = models.Todo(**todo_data)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def complete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    todo.completed = True
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return todo

# Reminder CRUD Operations
def create_reminder(db: Session, reminder_data: dict):
    reminder = models.Reminder(**reminder_data)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reminder).offset(skip).limit(limit).all()

def delete_reminder(db: Session, reminder_id: int):
    reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not reminder:
        return None
    db.delete(reminder)
    db.commit()
    return reminder

# Calendar Event CRUD Operations
def create_calendar_event(db: Session, event_data: dict):
    event = models.CalendarEvent(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_calendar_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CalendarEvent).offset(skip).limit(limit).all()

def delete_calendar_event(db: Session, event_id: int):
    event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not event:
        return None
    db.delete(event)
    db.commit()
    return event