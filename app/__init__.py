from fastapi import FastAPI
from app.core.extensions import engine, Base
from app.api.v1.auth_api import router as auth_router
from app.api.v1.user_api import router as user_router
from app.api.v1.workout_api import router as workout_router
from app.core.database import create_tables

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workout_router)


@app.on_event("startup")
async def startup_event():
    create_tables()
