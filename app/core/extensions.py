from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from app.data.repositories.user_repository import UserRepository
    try:
        user_id = int(user_id)
        user = UserRepository.get_user_by_id(user_id)
        return user
    except (ValueError, TypeError):
        return None
