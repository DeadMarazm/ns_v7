from flask import render_template, flash
from . import main_bp
from ...models.models import WOD


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': 'KIM'}
    # Получаем последние 3 тренировки
    wods_count = WOD.query.order_by(WOD.wod_name.desc()).all()
    # Получаем последние 3 тренировки
    wods = WOD.query.order_by(WOD.wod_name.desc()).limit(3).all()

    # Проверка, что wods не пустое
    if wods:
        return render_template('main/index.html', user=user, wods=wods, wods_count=wods_count, title='Домашняя')
    else:
        flash('Нет доступных тренировок.', 'warning')
        return render_template('main/index.html', user=user, wods=[], title='Домашняя')
