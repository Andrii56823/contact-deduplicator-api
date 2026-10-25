from fastapi import FastAPI
from database import SessionLocal, engine, Base
import models
from routers import users
from routers import contacts

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(contacts.router)