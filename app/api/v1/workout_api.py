from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import List
from app.api.v1.user_api import get_current_user
from app.data.repositories.workout_repository import WorkoutRepository
from app.domain.workout import Workout
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/workouts", tags=["workouts"])


class WorkoutCreate(BaseModel):
    """Модель для создания тренировки."""
    name: str
    warm_up: str
    workout: str
    description: str


@router.post("/", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Создание новой тренировки."""
    try:
        new_workout = Workout(name=workout.name, warm_up=workout.warm_up, workout=workout.workout,
                              description=workout.description)
        saved_workout = WorkoutRepository.save(db, new_workout)
        return saved_workout
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        print(f"Error in create_workout: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/", response_model=List[Workout], status_code=status.HTTP_200_OK)
async def read_workouts(db: Session = Depends(get_db)):
    """Получение списка тренировок."""
    try:
        workouts = WorkoutRepository.get_all(db)
        return workouts
    except Exception as e:
        print(f"Error in read_workouts: {e}")
        raise HTTPException(status_code=500, detail="Server error")
