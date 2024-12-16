from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms.forms import RegistrationForm, LoginForm
from . import auth_bp
from app.data.repositories.user_repository import UserRepository
from ...domain.user import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Маршрут для авторизации пользователя """
    form = LoginForm()
    if form.validate_on_submit():
        user = UserRepository.get_user_by_email(form.email.data)
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index_bp.index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """ Маршрут для выхода пользователя из системы """
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ Маршрут для регистрации пользователя """
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Создаем нового пользователя
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            UserRepository.save_user(user)
            login_user(user)
            flash('Вы успешно зарегистрированы!', 'success')
            return redirect(url_for('index_bp.index'))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('auth/register.html', form=form, title='Регистрация')
