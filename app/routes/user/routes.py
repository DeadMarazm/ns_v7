from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms.forms import EditProfileForm
from app.models.models import User
from . import user_bp


@user_bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    completed_wods = user.count_completed_wods()

    return render_template('user/profile.html', user=user, completed_wods=completed_wods)



@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('user_bp.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('user/edit_profile.html', title='Редактировать профиль',
                           form=form)
