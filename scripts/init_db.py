import os
import sys

# Добавляем корневую папку проекта в путь Python
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Map, Grenade, Video
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    # Создаем приложение
    app = create_app()
    
    with app.app_context():
        print("🗑️  Удаляем старые таблицы...")
        db.drop_all()
        
        print("🔄 Создаем новые таблицы...")
        db.create_all()
        
        print("👤 Добавляем тестового пользователя...")
        # Добавляем администратора
        admin_user = User(
            username='admin',
            email='admin@grenadeguide.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.flush()  # Получаем ID пользователя
        
        print("🗺️ Добавляем карты...")
        maps = [
            Map(name='de_mirage', display_name='Mirage'),
            Map(name='de_inferno', display_name='Inferno'),
            Map(name='de_dust2', display_name='Dust II'),
            Map(name='de_nuke', display_name='Nuke'),
            Map(name='de_vertigo', display_name='Vertigo')
        ]
        
        for map_obj in maps:
            db.session.add(map_obj)
        
        print("💣 Добавляем гранаты...")
        grenades = [
            Grenade(name='smoke', display_name='Smoke Grenade', color='success'),
            Grenade(name='flash', display_name='Flashbang', color='warning'),
            Grenade(name='he', display_name='HE Grenade', color='danger'),
            Grenade(name='molotov', display_name='Molotov', color='danger')
        ]
        
        for grenade in grenades:
            db.session.add(grenade)
        
        # Сохраняем чтобы получить ID
        db.session.commit()
        
        print("🎥 Добавляем тестовые видео...")
        # Теперь получаем объекты с ID
        dust2_map = Map.query.filter_by(name='de_dust2').first()
        smoke_grenade = Grenade.query.filter_by(name='smoke').first()
        admin_user = User.query.filter_by(username='admin').first()
        
        print(f"🔍 Dust2 ID: {dust2_map.id}, Smoke ID: {smoke_grenade.id}, Admin ID: {admin_user.id}")
        
        test_videos = [
            {
                'title': 'Smoke from T Spawn to B Site',
                'description': 'Быстрый смок с T спавна на B площадку. Идеально для быстрого захвата B.',
                'video_url': 'https://www.youtube.com/embed/w2qgKREtsDs',
                'thumbnail_url': 'https://img.youtube.com/vi/w2qgKREtsDs/hqdefault.jpg'
            },
            {
                'title': 'Mid to Xbox Smoke',
                'description': 'Смок из миддла на Xbox. Закрывает обзор снайперам с A сайта.',
                'video_url': 'https://www.youtube.com/embed/z9xyfO5jPkI',
                'thumbnail_url': 'https://img.youtube.com/vi/z9xyfO5jPkI/mqdefault.jpg'
            },
            {
                'title': 'Long A Smoke from CT',
                'description': 'Защитный смок на лонг А с позиции CT. Помогает удерживать лонг.',
                'video_url': 'https://www.youtube.com/embed/4Pz6lUtuqvo',
                'thumbnail_url': 'https://img.youtube.com/vi/4Pz6lUtuqvo/hqdefault.jpg'
            },
            {
                'title': 'A Site Cross Smoke',
                'description': 'Смок для перехода через A сайт. Безопасный переход под прикрытием дыма.',
                'video_url': 'https://www.youtube.com/embed/XbKWPRDHmWY',
                'thumbnail_url': 'https://img.youtube.com/vi/XbKWPRDHmWY/hqdefault.jpg'
            },
            {
                'title': 'B Tunnels Smoke',
                'description': 'Смок для блокировки туннелей B. Контроль над подходами к B сайту.',
                'video_url': 'https://www.youtube.com/embed/EjjCIvnnwds',
                'thumbnail_url': 'https://img.youtube.com/vi/EjjCIvnnwds/hqdefault.jpg'
            },
            {
                'title': 'CT Spawn to Mid Smoke',
                'description': 'Смок с CT спавна в миддл. Задержка выхода террористов.',
                'video_url': 'https://www.youtube.com/embed/Jk4657WJX40',
                'thumbnail_url': 'https://img.youtube.com/vi/Jk4657WJX40/hqdefault.jpg'
            }
        ]
        
        for video_data in test_videos:
            video = Video(
                title=video_data['title'],
                description=video_data['description'],
                video_url=video_data['video_url'],
                thumbnail_url=video_data['thumbnail_url'],
                author_id=admin_user.id,
                map_id=dust2_map.id,
                grenade_id=smoke_grenade.id,
                created_at=datetime.utcnow()
            )
            db.session.add(video)
        
        # Финальное сохранение
        db.session.commit()
        
        # Проверяем результат
        maps_count = Map.query.count()
        grenades_count = Grenade.query.count()
        videos_count = Video.query.count()
        users_count = User.query.count()
        
        print("\n✅ База данных успешно инициализирована!")
        print(f"📊 Статистика:")
        print(f"   🗺️  Карты: {maps_count}")
        print(f"   💣 Гранаты: {grenades_count}")
        print(f"   🎥 Видео: {videos_count}")
        print(f"   👤 Пользователи: {users_count}")
        print(f"\n🔑 Тестовый пользователь: admin / admin123")
        print(f"🎯 Тестовые видео: Dust II + Smoke Grenade (ID: {dust2_map.id} + {smoke_grenade.id})")

if __name__ == '__main__':
    init_database()