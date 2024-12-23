from app.core.extensions import SessionLocal, engine, Base


def get_db():
    """Функция зависимостей для получения сеанса работы с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создает таблицы базы данных."""
    Base.metadata.create_all(bind=engine)
