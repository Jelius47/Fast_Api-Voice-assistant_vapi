fastapi-voice-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic models
│   ├── crud.py              # Database operations
│   ├── dependencies.py       # Dependency injections
│   ├── routers/             # API routers
│   │   ├── __init__.py
│   │   ├── todos.py         # Todo-related endpoints
│   │   ├── reminders.py     # Reminder-related endpoints
│   │   └── calendar.py      # Calendar-related endpoints
│   └── utils.py             # Utility functions
│
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
└── README.md                # Project documentation