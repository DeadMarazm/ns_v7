from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/api/v1/users", tags=["users"])


# Заглушка для получения текущего пользователя
async def get_current_user(token: str = Depends(None)):
    # В реальном приложении здесь будет декодирование токена
    return {"id": 1, "username": "testuser"}


@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    """
    return current_user


@router.get("/profile/{user_id}")
async def read_user_profile(user_id: int):
    """
    Получение публичного профиля пользователя.
    """
    # Пример заглушки
    user = {"id": user_id, "username": f"user_{user_id}", "public_profile": "some info"}
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
