# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements/base.txt requirements/base.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements/base.txt

# Копируем код приложения
COPY . .

# Переменные окружения
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV SECRET_KEY=your-secret-key-here

# Создаем папку для базы данных и назначаем права
RUN mkdir -p /app/instance && chown -R nobody:nogroup /app/instance

# Переключаемся на непривилегированного пользователя
USER nobody

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["flask", "run", "--host=0.0.0.0"]