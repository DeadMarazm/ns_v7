import pytest
from flask import url_for
from app.data.models import ResultModel, WorkoutModel
from app import db
from datetime import datetime


@pytest.mark.usefixtures("client", "app_context")
class TestWorkoutRoutes:
    """Тестирование маршрутов, связанных с тренировками."""

    @pytest.fixture(autouse=True)
    def setup(self, client, test_user):
        """Настройка данных для тестов."""
        self.client = client
        self.user = test_user
        self.wod1 = WorkoutModel(name='Test Workout 1', warm_up='Test Warm-up 1', workout='Test Workout 1',
                                 description='Test Description 1', date_posted=datetime.now())
        self.wod2 = WorkoutModel(name='Test Workout 2', warm_up='Test Warm-up 2', workout='Test Workout 2',
                                 description='Test Description 2', date_posted=datetime.now())
        db.session.add(self.wod1)
        db.session.add(self.wod2)
        db.session.commit()

    def login(self, email, password):
        """Вспомогательная функция login для пользователя"""
        return self.client.post(url_for('auth_bp.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Вспомогательная функция logout для пользователя"""
        return self.client.get(url_for('auth_bp.logout'), follow_redirects=True)

    def test_workout_list_route(self):
        """ Тест маршрута: список тренировок """
        response = self.client.get(url_for('workout_bp.workouts_list'))
        assert response.status_code == 200
        # Проверяем наличие данных в ответе
        assert self.wod1.name.encode('utf-8') in response.data
        assert self.wod2.name.encode('utf-8') in response.data

    def test_workout_detail_route_get(self):
        """ Тестирование страницы с детальной информацией о тренировке (GET-запрос) """
        # Тест с авторизованным пользователем
        self.login('test@example.com', 'testpassword')
        response = self.client.get(url_for('workout_bp.workout_detail', id=self.wod1.id))
        assert response.status_code == 200

        # Проверяем наличие ключевых элементов на странице (авторизован)
        assert self.wod1.name.encode('utf-8') in response.data
        assert self.wod1.warm_up.encode('utf-8') in response.data
        assert self.wod1.workout.encode('utf-8') in response.data
        assert self.wod1.description.encode('utf-8') in response.data
        assert 'Эту тренировку выполнили: 0 раз(а)'.encode('utf-8') in response.data

        self.logout()

        # Тест с неавторизованным пользователем (сначала GET, затем POST для появления сообщения)
        response = self.client.get(url_for('workout_bp.workout_detail', id=self.wod1.id))  # GET запрос
        assert response.status_code == 200

        response = self.client.post(url_for('workout_bp.workout_detail', id=self.wod1.id),
                                    data={
                                        'result': True,
                                        'submit': 'Подтвердить'
                                    }, follow_redirects=True)
        assert response.status_code == 200
        assert 'Пожалуйста, войдите в систему для подтверждения тренировки.'.encode('utf-8') in response.data

    def test_workout_detail_route_post_authenticated(self):
        """ Тест маршрута: подтверждение выполнения тренировки (POST-запрос, авторизован) """
        self.login('test@example.com', 'testpassword')

        # Отправляем POST-запрос с данными формы
        response = self.client.post(
            url_for('workout_bp.workout_detail', id=self.wod1.id),
            data={
                'result': 'y',  # Значение для checkbox должно быть 'y'
                'submit': 'Подтвердить'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert 'Поздравляем с выполнением тренировки!'.encode('utf-8') in response.data

        result = ResultModel.query.filter_by(
            user_id=self.user.id,
            workout_id=self.wod1.id
        ).first()
        assert result is not None
        assert result.confirm
        self.logout()
