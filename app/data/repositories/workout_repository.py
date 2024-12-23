from datetime import datetime
from typing import Optional
from app.data.models import Workout as WorkoutModel
from app.domain.workout import Workout
from sqlalchemy.orm import Session


class WorkoutRepository:
    """Репозиторий для работы с тренировками."""

    @staticmethod
    def get_by_id(db: Session, workout_id: int) -> Optional[Workout]:
        """Получение тренировки по ID."""
        try:
            workout_model = db.query(WorkoutModel).get(workout_id)
            return WorkoutRepository._convert_to_domain(workout_model)
        except Exception as e:
            print(f"Error in get_by_id: {e}")
            return None

    @staticmethod
    def get_all(db: Session) -> list[Workout]:
        """Получение всех тренировок."""
        try:
            workout_models = db.query(WorkoutModel).order_by(WorkoutModel.date_posted.desc()).all()
            return [WorkoutRepository._convert_to_domain(workout) for workout in workout_models]
        except Exception as e:
            print(f"Error in get_all: {e}")
            return []

    @staticmethod
    def save(db: Session, workout: Workout) -> Workout:
        """Сохранение тренировки."""
        try:
            workout_model = db.query(WorkoutModel).get(workout.id)

            if workout_model:
                WorkoutRepository._update_existing(db, workout_model, workout)
            else:
                WorkoutRepository._create_new(db, workout)

            db.commit()
            return WorkoutRepository._convert_to_domain(workout_model)
        except Exception as e:
            db.rollback()
            print(f"Error in save: {e}")
            raise

    @staticmethod
    def delete(db: Session, workout_id: int) -> bool:
        """Удаление тренировки."""
        try:
            workout_model = db.query(WorkoutModel).get(workout_id)
            if not workout_model:
                raise ValueError(f"Workout with id {workout_id} does not exist.")
            db.delete(workout_model)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error in delete: {e}")
            raise

    @staticmethod
    def get_by_date(db: Session, start_date: datetime, end_date: datetime):
        """Получение тренировок по дате."""
        try:
            workout_models = db.query(WorkoutModel).filter(WorkoutModel.date_posted.between(start_date, end_date)).all()
            return [WorkoutRepository._convert_to_domain(wm) for wm in workout_models]
        except Exception as e:
            print(f"Error in get_by_date: {e}")
            return []

    @staticmethod
    def _convert_to_domain(workout_model: WorkoutModel) -> Optional[Workout]:
        """Преобразование модели в доменный объект."""
        if not workout_model:
            return None
        return Workout(
            id=workout_model.id,
            name=workout_model.name or workout_model.date_posted.strftime('%Y-%m-%d'),
            warm_up=workout_model.warm_up,
            workout=workout_model.workout,
            description=workout_model.description,
            date_posted=workout_model.date_posted
        )

    @staticmethod
    def _update_existing(db: Session, workout_model: WorkoutModel, workout: Workout):
        """Обновление существующей тренировки."""
        workout_model.name = workout.name
        workout_model.warm_up = workout.warm_up
        workout_model.workout = workout.workout
        workout_model.description = workout.description
        workout_model.date_posted = workout.date_posted

    @staticmethod
    def _create_new(db: Session, workout: Workout):
        """Создание новой тренировки."""
        workout_model = WorkoutModel(
            name=workout.name,
            warm_up=workout.warm_up,
            workout=workout.workout,
            description=workout.description,
            date_posted=workout.date_posted
        )
        db.add(workout_model)
        db.flush()
        workout.id = workout_model.id
