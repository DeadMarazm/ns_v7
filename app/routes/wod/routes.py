from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import WOD, ResultBool
from . import wod_bp
from ...forms.forms import ResultBoolForm


@wod_bp.route('/wods')
def wod_list():
    wods_list = WOD.query.order_by(WOD.wod_name.desc()).all()
    return render_template('wod/wods_list.html',
                           wods_list=wods_list, title='Список тренировок')


@wod_bp.route('/wods/<int:id>', methods=['GET', 'POST'])
def wod_detail(id):
    wod_detail = WOD.query.get_or_404(id)
    result_bool_form = ResultBoolForm()

    if result_bool_form.validate_on_submit():
        if current_user.is_authenticated:
            result = ResultBool(confirm=result_bool_form.result.data,
                                user_id=current_user.id,
                                wod_id=id)
            db.session.add(result)
            db.session.commit()
            flash('Поздравляем с выполнением тренировки!')
        else:
            flash('Пожалуйста, войдите в систему для подтверждения тренировки.')
        return redirect(url_for('wod_bp.wod_detail', id=id))

    # Проверка, аутентифицирован ли пользователь
    if current_user.is_authenticated:
        results = ResultBool.query.filter_by(wod_id=id, user_id=current_user.id) \
            .order_by(ResultBool.date_posted.desc()).first()
    else:
        results = None

    # Если результата нет, создаем заглушку
    if not results:
        results = ResultBool(confirm=False)

    # Получаем общее количество выполнений
    total_completions = wod_detail.get_total_completions()

    return render_template('wod/wod_detail.html', detail=wod_detail, result_bool_form=result_bool_form,
                           results=results, total_completions=total_completions)


@wod_bp.route('/wods/<int:id>/confirm')
@login_required
def wod_confirm(id):
    wod = WOD.query.get_or_404(id)
    wod.confirm = True
    db.session.commit()
    flash('Вы подтвердили тренировку!')
    return redirect(url_for('wod_bp.wod_detail', id=id))
