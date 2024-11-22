from fastapi import FastAPI, Depends
from typing import Annotated
import models
from database import engine, SessionLocal
from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
