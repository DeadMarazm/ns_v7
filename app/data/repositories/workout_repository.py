from datetime import datetime
from typing import Optional
from app.data.models import WorkoutModel, db
from app.domain.workout import Workout


class WorkoutRepository:

    @staticmethod
    def get_by_id(workout_id: int) -> Optional[Workout]:
        workout_model = WorkoutModel.query.get(workout_id)
        return WorkoutRepository._convert_to_domain(workout_model)

    @staticmethod
    def get_all() -> list[Workout]:
        workout_models = WorkoutModel.query.order_by(WorkoutModel.date_posted.desc()).all()
        return [WorkoutRepository._convert_to_domain(workout) for workout in workout_models]

    @staticmethod
    def save(workout: Workout) -> Workout:
        workout_model = WorkoutModel.query.get(workout.id)

        if workout_model:
            WorkoutRepository._update_existing(workout_model, workout)
        else:
            WorkoutRepository._create_new(workout)

        db.session.commit()
        return workout

    @staticmethod
    def delete(workout_id: int) -> bool:
        workout_model = WorkoutModel.query.get(workout_id)
        if not workout_model:
            raise ValueError(f"Workout with id {workout_id} does not exist.")
        db.session.delete(workout_model)
        db.session.commit()
        return True

    @staticmethod
    def get_by_date(start_date: datetime, end_date: datetime):
        workout_models = WorkoutModel.query.filter(WorkoutModel.date_posted.between(start_date, end_date)).all()
        return [WorkoutRepository._convert_to_domain(wm) for wm in workout_models]

    @staticmethod
    def _convert_to_domain(workout_model: WorkoutModel) -> Optional[Workout]:
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
    def _update_existing(workout_model: WorkoutModel, workout: Workout):
        workout_model.name = workout.name
        workout_model.warm_up = workout.warm_up
        workout_model.workout = workout.workout
        workout_model.description = workout.description
        workout_model.date_posted = workout.date_posted

    @staticmethod
    def _create_new(workout: Workout):
        workout_model = WorkoutModel(
            name=workout.name,
            warm_up=workout.warm_up,
            workout=workout.workout,
            description=workout.description,
            date_posted=workout.date_posted
        )
        db.session.add(workout_model)
        db.session.flush()
        workout.id = workout_model.id
