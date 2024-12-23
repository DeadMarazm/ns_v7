from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.database import get_db
from app.data.models import User
from config.api_config import APIConfig
from app.data.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/v1/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=APIConfig.OAUTH2_TOKEN_URL)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Получение текущего пользователя из токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, APIConfig.SECRET_KEY, algorithms=[APIConfig.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        user = UserRepository.get_by_username(db, username)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"Error in get_current_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(current_user=Depends(get_current_user)):
    """Получение информации о текущем пользователе."""
    return current_user


@router.get("/profile/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Получение публичного профиля пользователя."""
    try:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print(f"Error in read_user_profile: {e}")
        raise HTTPException(status_code=500, detail="Server error")
