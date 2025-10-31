import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    # Секретный ключ для безопасности (из .env или значение по умолчанию)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    
    # URL для подключения к БД (из .env или SQLite по умолчанию)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'grenade_guide.db')
    
    # Отключаем систему отслеживания модификаций (экономит память)
    SQLALCHEMY_TRACK_MODIFICATIONS = False