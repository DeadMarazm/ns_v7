from flask.cli import with_appcontext
import click
from app.extensions import db
from app.models.models import User, Role, WOD
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command(name='shell')
@with_appcontext
def shell():
    import code
    from flask import current_app
    shell_context = dict(db=db, app=current_app, User=User, Role=Role, WOD=WOD)
    code.interact(local=shell_context)


@click.command(name='create_wods')
@with_appcontext
def create_wods():
    """Создает тестовые тренировки в базе данных"""
    for i in range(1, 6):
        wod = WOD(
            wod_name=f"Тренировка {i}",
            warm_up=f"Разминка {i}",
            workout=f"Основной комплекс {i}",
            description=f"Описание тренировки {i}",
            date_posted=datetime.now()
        )
        db.session.add(wod)
        logger.info(f"Добавлена тренировка: {wod.wod_name}")
    db.session.commit()
    count = WOD.query.count()
    logger.info(f"Всего тренировок после добавления: {count}")
    logger.info("Тренировки созданы!")
