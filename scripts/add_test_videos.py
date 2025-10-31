import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models import Video, User, Map, Grenade
from datetime import datetime

def add_test_videos():
    app = create_app()
    with app.app_context():
        # Находим нужные сущности в базе
        dust2_map = Map.query.filter_by(name='de_dust2').first()
        smoke_grenade = Grenade.query.filter_by(name='smoke').first()
        admin_user = User.query.filter_by(username='user').first()
        
        if not dust2_map or not smoke_grenade or not admin_user:
            print("Ошибка: не найдены необходимые данные в базе!")
            return
        
        # Проверяем, есть ли уже видео
        existing_videos = Video.query.filter_by(map_id=dust2_map.id, grenade_id=smoke_grenade.id).count()
        if existing_videos > 0:
            print(f"Видео для Dust2 Smoke уже существуют ({existing_videos} шт.)")
            return
        
        # Добавляем тестовые видео
        test_videos = [
            {
                'title': 'Smoke from T Spawn to B Site',
                'description': 'Быстрый смок с T спавна на B площадку. Идеально для быстрого захвата B.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Заглушка
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+B+Smoke'
            },
            {
                'title': 'Mid to Xbox Smoke',
                'description': 'Смок из миддла на Xbox. Закрывает обзор снайперам с A сайта.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+Mid+Smoke'
            },
            {
                'title': 'Long A Smoke from CT',
                'description': 'Защитный смок на лонг А с позиции CT. Помогает удерживать лонг.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+Long+Smoke'
            },
            {
                'title': 'A Site Cross Smoke',
                'description': 'Смок для перехода через A сайт. Безопасный переход под прикрытием дыма.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+A+Cross'
            },
            {
                'title': 'B Tunnels Smoke',
                'description': 'Смок для блокировки туннелей B. Контроль над подходами к B сайту.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+B+Tunnels'
            },
            {
                'title': 'CT Spawn to Mid Smoke',
                'description': 'Смок с CT спавна в миддл. Задержка выхода террористов.',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': 'https://via.placeholder.com/300x200/28a745/ffffff?text=Dust2+Mid+CT'
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
                grenade_id=smoke_grenade.id
            )
            db.session.add(video)
        
        db.session.commit()
        print(f"Добавлено {len(test_videos)} тестовых видео для Dust2 Smoke!")

if __name__ == '__main__':
    add_test_videos()