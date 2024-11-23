from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Инициализация расширений
db = SQLAlchemy()  # Инициализация SQLAlchemy для работы с базой данных
migrate = Migrate()  # Инициализация Flask-Migrate для миграций базы данных
bootstrap = Bootstrap()  # Инициализация Flask-Bootstrap для использования Bootstrap стилей
login_manager = LoginManager()  # Инициализация Flask-Login для управления сессиями пользователей


# Функция для загрузки пользователя из базы данных
@login_manager.user_loader
def load_user(user_id):
    from app.models.models import User  # Импорт модели User здесь, чтобы избежать циклического импорта
    return User.query.get(user_id)  # Возвращаем пользователя по его ID
