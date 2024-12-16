from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from typing import Dict
from pydantic import BaseModel
from config.api_config import APIConfig  # Импортируем конфиг
from app.data.repositories.user_repository import UserRepository
from app.domain.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=APIConfig.OAUTH2_TOKEN_URL)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


def is_valid_credentials(username: str, password: str) -> bool:
    """Проверяет, действительны ли учетные данные"""
    user = UserRepository.get_by_username(username)
    return user and user.check_password(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Создание JWT токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=APIConfig.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, APIConfig.SECRET_KEY, algorithm=APIConfig.ALGORITHM)


def user_exists(email: str) -> bool:
    """Проверяет, существует ли пользователь с данным email"""
    return UserRepository.get_by_email(email) is not None


def create_user(user_data: UserCreate) -> User:
    """Создает нового пользователя"""
    user = User(username=user_data.username, email=user_data.email, password=user_data.password)
    user.set_password(user_data.password)
    return UserRepository.save(user)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    """
    Логин пользователя. Возвращает токен доступа.
    """
    if not is_valid_credentials(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(user_data: UserCreate) -> Dict:
    """
    Регистрация нового пользователя.
    """
    if user_exists(user_data.email):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(user_data)
    return {"message": "User successfully registered", "user_id": new_user.id}
