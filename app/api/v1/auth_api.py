from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from typing import Dict
from pydantic import BaseModel, ValidationError
from config.api_config import APIConfig
from app.data.repositories.user_repository import UserRepository
from app.domain.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session
import bcrypt

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=APIConfig.OAUTH2_TOKEN_URL)


class UserCreate(BaseModel):
    """Модель для создания пользователя."""
    username: str
    email: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Создание JWT токена."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=APIConfig.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, APIConfig.SECRET_KEY, algorithm=APIConfig.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """Проверка пароля."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@router.post("/token", response_model=Dict, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Dict:
    """Логин пользователя."""
    try:
        user = UserRepository.get_by_username(db, form_data.username)
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/register", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация пользователя."""
    try:
        if UserRepository.get_by_username(db, user_data.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        if UserRepository.get_by_email(db, user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = User(username=user_data.username, email=user_data.email, password_hash=hashed_password.decode('utf-8'))
        saved_user = UserRepository.save_user(db, user)
        return {"message": "User successfully registered", "user_id": saved_user.id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        print(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Server error")
