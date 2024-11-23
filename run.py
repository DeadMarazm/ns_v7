from app import create_app

# Создаем приложение
app = create_app()

# Запускаем сервер разработки Flask
if __name__ == "__main__":
    app.run(debug=True)
