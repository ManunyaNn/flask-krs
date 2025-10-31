from app import create_app

# Создаем приложение используя фабрику
app = create_app()

# Запускаем приложение только если файл запущен напрямую
if __name__ == '__main__':
    app.run(debug=True)  # debug=True включает режим отладки