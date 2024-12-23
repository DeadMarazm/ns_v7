from typing import Optional
from sqlalchemy.orm import Session
from app.data.models import Result as ResultModel
from app.domain.result import Result


class ResultRepository:
    """Репозиторий для работы с результатами тренировок."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, result_id: int) -> Optional[Result]:
        """Получение результата по ID."""
        try:
            result_model = self.db.query(ResultModel).filter(ResultModel.id == result_id).first()
            return self._convert_to_domain(result_model)
        except Exception as e:
            print(f"Error in get_by_id: {e}")
            return None

    def get_by_user(self, user_id: int) -> list[Result]:
        """Получение результатов пользователя."""
        try:
            result_models = self.db.query(ResultModel).filter(ResultModel.user_id == user_id).all()
            return [self._convert_to_domain(result) for result in result_models]
        except Exception as e:
            print(f"Error in get_by_user: {e}")
            return []

    def get_by_workout(self, workout_id: int) -> list[Result]:
        """Получение результатов тренировки."""
        try:
            result_models = self.db.query(ResultModel).filter(ResultModel.workout_id == workout_id).all()
            return [self._convert_to_domain(result) for result in result_models]
        except Exception as e:
            print(f"Error in get_by_workout: {e}")
            return []

    def get_by_user_and_workout(self, user_id: int, workout_id: int) -> Optional[Result]:
        """Получение результата пользователя для конкретной тренировки."""
        try:
            result_model = self.db.query(ResultModel).filter(
                ResultModel.user_id == user_id,
                ResultModel.workout_id == workout_id
            ).order_by(ResultModel.date_posted.desc()).first()
            return self._convert_to_domain(result_model)
        except Exception as e:
            print(f"Error in get_by_user_and_workout: {e}")
            return None

    def save(self, result: Result) -> Result:
        """Сохранение результата."""
        try:
            result_model = ResultModel(
                user_id=result.user_id,
                workout_id=result.workout_id,
                confirm=result.confirm,
                date_posted=result.date_posted
            )
            self.db.add(result_model)
            self.db.commit()
            self.db.refresh(result_model)
            return self._convert_to_domain(result_model)
        except Exception as e:
            self.db.rollback()
            print(f"Error in save: {e}")
            raise

    def delete(self, result_id: int) -> bool:
        """Удаление результата."""
        try:
            result_model = self.db.query(ResultModel).filter(ResultModel.id == result_id).first()
            if not result_model:
                raise ValueError(f"Result with id {result_id} does not exist.")
            self.db.delete(result_model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error in delete: {e}")
            raise

    @staticmethod
    def _convert_to_domain(result_model: ResultModel) -> Optional[Result]:
        """Преобразование модели в доменный объект."""
        if not result_model:
            return None

        return Result(
            id=result_model.id,
            user_id=result_model.user_id,
            workout_id=result_model.workout_id,
            confirm=result_model.confirm,
            date_posted=result_model.date_posted
        )
