# ns_v7
1. Библиотеки: requirements/base
pip install -r requirements/base.txt
pip freeze > requirements/base.txt

2. Команды:
БД:
flask db init
flask db migrate
flask db migrate -m "#"
flask db upgrade

Генерация 5 Тренировок Дня:
flask create_workouts

Генерация 3 Пользователей:
flask create_users

Удаление файла базы данных
flask delete_db

3. Тесты:
Запуск:
pytest

4. Работа с git
git checkout master
git pull origin master


5. Docker
Старт: docker-compose up --build

docker build -t ns_v7_image .
docker run --name ns_v7_container -p 5000:5000 ns_v7_image
docker-compose up --build
docker logs name ns_v7_container -f


6. запуск проекта run.py






