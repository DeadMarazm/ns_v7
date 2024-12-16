from typing import Optional
from app.data.models import ResultModel, db
from app.domain.result import Result


class ResultRepository:
    @staticmethod
    def get_by_id(result_id: int) -> Optional[Result]:
        result_model = ResultModel.query.get(result_id)
        return ResultRepository._convert_to_domain(result_model)

    @staticmethod
    def get_by_user(user_id: int) -> list[Result]:
        result_models = ResultModel.query.filter_by(user_id=user_id).all()
        return [ResultRepository._convert_to_domain(result) for result in result_models]

    @staticmethod
    def get_by_workout(workout_id: int) -> list[Result]:
        result_models = ResultModel.query.filter_by(workout_id=workout_id).all()
        return [ResultRepository._convert_to_domain(result) for result in result_models]

    @staticmethod
    def get_by_user_and_workout(user_id: int, workout_id: int) -> Optional[Result]:
        result_models = ResultModel.query.filter(
            ResultModel.user_id == user_id,
            ResultModel.workout_id == workout_id
        ).order_by(ResultModel.date_posted.desc()).all()
        return ResultRepository._convert_to_domain(result_models[0]) if result_models else None

    @staticmethod
    def save(result: Result) -> Result:
        result_model = ResultModel.query.get(result.id)

        if result_model:
            ResultRepository._update_existing(result_model, result)
        else:
            ResultRepository._create_new(result)

        db.session.commit()
        return result

    @staticmethod
    def delete(result_id: int) -> bool:
        result_model = ResultModel.query.get(result_id)
        if not result_model:
            raise ValueError(f"Result with id {result_id} does not exist.")
        db.session.delete(result_model)
        db.session.commit()
        return True

    @staticmethod
    def _convert_to_domain(result_model: ResultModel) -> Optional[Result]:
        if not result_model:
            return None

        return Result(
            id=result_model.id,
            user_id=result_model.user_id,
            workout_id=result_model.workout_id,
            confirm=result_model.confirm,
            date_posted=result_model.date_posted
        )

    @staticmethod
    def _update_existing(result_model: ResultModel, result: Result):
        result_model.confirm = result.confirm
        result_model.user_id = result.user_id
        result_model.workout_id = result.workout_id
        result_model.date_posted = result.date_posted

    @staticmethod
    def _create_new(result: Result):
        result_model = ResultModel(
            user_id=result.user_id,
            workout_id=result.workout_id,
            confirm=result.confirm,
            date_posted=result.date_posted
        )
        db.session.add(result_model)
        db.session.flush()
        result.id = result_model.id
