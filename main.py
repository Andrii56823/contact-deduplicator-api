from fastapi import FastAPI
from database import SessionLocal, engine, Base, get_db
import models
from routers import users
from routers import contacts


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(contacts.router)