from typing import Optional
from sqlalchemy.orm import Session
from app.domain.user import User
from app.data.models import User as UserModel


class UserRepository:
    """Репозиторий для работы с пользователями."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Получение пользователя по ID."""
        try:
            return db.query(UserModel).filter(UserModel.id == user_id).first()
        except Exception as e:
            print(f"Error in get_user_by_id: {e}")
            return None

    @staticmethod
    def get_by_username(db: Session, username: str):
        """Получение пользователя по имени пользователя."""
        try:
            return db.query(UserModel).filter(UserModel.username == username).first()
        except Exception as e:
            print(f"Error in get_by_username: {e}")
            return None

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Получение пользователя по email."""
        try:
            user_model = db.query(UserModel).filter_by(email=email).first()
            return UserRepository._convert_to_domain(user_model)
        except Exception as e:
            print(f"Error in get_by_email: {e}")
            return None

    @staticmethod
    def save_user(db: Session, user: User):
        """Сохранение пользователя."""
        try:
            user_model = UserModel(
                id=user.id,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                active=user.active,
                confirmed_at=user.confirmed_at,
                uuid=user.uuid
            )
            db.add(user_model)
            db.commit()
            db.refresh(user_model)
            return UserRepository._convert_to_domain(user_model)

        except Exception as e:
            db.rollback()
            print(f"Error in save_user: {e}")
            raise

    @staticmethod
    def _convert_to_domain(user_model: UserModel) -> Optional[User]:
        """Преобразование модели в доменный объект."""
        if not user_model:
            return None

        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password_hash,
            active=user_model.active,
            confirmed_at=user_model.confirmed_at,
            uuid=user_model.uuid
        )
