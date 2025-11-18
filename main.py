from fastapi import FastAPI
from auth_router import auth_router
import db as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="Auth Service")
app.include_router(auth_router)