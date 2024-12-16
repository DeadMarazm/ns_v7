from typing import Optional
from werkzeug.security import generate_password_hash
from app.data.models import UserModel, db
from app.domain.user import User


class UserRepository:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        user_model = UserModel.query.get(user_id)
        return UserRepository._convert_to_domain(user_model)

    @staticmethod
    def save_user(user: User) -> User:
        user_model = UserModel.query.get(user.id)

        if user_model:
            UserRepository._update_existing_user(user_model, user)
        else:
            UserRepository._create_new_user(user)

        db.session.commit()
        return user

    @staticmethod
    def _convert_to_domain(user_model: UserModel) -> Optional[User]:
        if not user_model:
            return None

        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password_hash,
            active=user_model.active,
            confirmed_at=user_model.confirmed_at
        )

    @staticmethod
    def _update_existing_user(user_model: UserModel, user: User):
        user_model.username = user.username
        user_model.email = user.email
        if user.password:
            user_model.password_hash = generate_password_hash(user.password)

    @staticmethod
    def _create_new_user(user: User):
        UserRepository._validate_unique_fields(user)

        user_model = UserModel(
            username=user.username,
            email=user.email,
            password_hash=generate_password_hash(user.password) if user.password else None,
            active=user.active,
            confirmed_at=user.confirmed_at
        )
        db.session.add(user_model)
        db.session.flush()
        user.id = user_model.id

    class UserAlreadyExistsError(Exception):
        pass

    @staticmethod
    def _validate_unique_fields(user: User):
        if UserModel.query.filter_by(username=user.username).first():
            raise UserAlreadyExistsError(f"Username '{user.username}' already exists")

