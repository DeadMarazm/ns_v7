import bcrypt as bcrypt

from app.data.repositories.user_repository import UserRepository
from app.domain.user import User
from sqlalchemy.orm import Session


class UserService:
    """Сервис для работы с пользователями."""

    @staticmethod
    def get_user_by_id(db: Session, user_id):
        """Получение пользователя по ID."""
        try:
            return UserRepository.get_user_by_id(db, user_id)
        except Exception as e:
            print(f"Error in get_user_by_id: {e}")
            return None

    @staticmethod
    def get_user_by_username(db: Session, username):
        """Получение пользователя по имени пользователя."""
        try:
            return UserRepository.get_by_username(db, username)
        except Exception as e:
            print(f"Error in get_user_by_username: {e}")
            return None

    @staticmethod
    def get_user_by_email(db: Session, email):
        """Получение пользователя по email."""
        try:
            return UserRepository.get_by_email(db, email)
        except Exception as e:
            print(f"Error in get_user_by_email: {e}")
            return None

    @staticmethod
    def create_user(db: Session, username, email, password):
        """Создание пользователя."""
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(
                id=None,
                username=username,
                email=email,
                password_hash=hashed_password.decode('utf-8'),
                active=True,
                confirmed_at=None
            )
            return UserRepository.save_user(db, user)
        except Exception as e:
            print(f"Error in create_user: {e}")
            raise

    @staticmethod
    def save_user(db: Session, user):
        """Сохранение пользователя."""
        try:
            UserRepository.save_user(db, user)
        except Exception as e:
            print(f"Error in save_user: {e}")
            raise

    @staticmethod
    def update_user(db: Session, user):
        """Обновление пользователя."""
        try:
            UserRepository.save_user(db, user)  # нужно переписать
        except Exception as e:
            print(f"Error in update_user: {e}")
            raise
