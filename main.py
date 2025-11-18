from fastapi import FastAPI
from auth_router import auth_router
from profiles_router import profiles_router
import db as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(profiles_router)