from flask import Flask
from config.config import AppConfig
from app.core.extensions import (
    db, migrate, bootstrap,
    login_manager, csrf
)


def create_app(config_class=AppConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    _init_extensions(app)
    _register_blueprints(app)
    _register_commands(app)

    return app


def _init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице.'


def _register_blueprints(app):
    from app.routes.index import index_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.workout import workout_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(workout_bp)


def _register_commands(app):
    from app.utils.commands import (
        shell, create_workouts,
        create_users, delete_db
    )

    app.cli.add_command(shell)
    app.cli.add_command(create_workouts)
    app.cli.add_command(create_users)
    app.cli.add_command(delete_db)
