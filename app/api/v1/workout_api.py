from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/api/v1/workouts", tags=["workouts"])


async def get_current_user(token: str = Depends(None)):
    return {"id": 1, "username": "testuser"}


class WorkoutCreate(BaseModel):
    name: str
    warm_up: str
    workout: str
    description: str


@router.post("/")
async def create_workout(workout: WorkoutCreate, current_user=Depends(get_current_user)):
    """
    Создать новую тренировку.
    """
    new_workout = {"id": 1, "name": workout.name, "user_id": current_user["id"]}
    return new_workout


@router.get("/")
async def read_workouts(current_user=Depends(get_current_user), skip: int = 0, limit: int = 10) -> List[dict]:
    """
    Получить список тренировок пользователя.
    """
    workouts = [{"id": i, "name": f"Workout {i}", "user_id": current_user["id"]} for i in range(skip, skip + limit)]
    return workouts
